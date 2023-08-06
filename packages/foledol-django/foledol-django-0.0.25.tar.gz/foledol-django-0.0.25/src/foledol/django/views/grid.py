import io

import xlsxwriter
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.expressions import RawSQL, F
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _
from foledol.django.logger import log
from foledol.django.models import Grid, ConditionGroup, Condition
from foledol.django.reports.grid import GridReport
from foledol.django.templatetags.form_extras import value
from foledol.django.tools.field import TextField, BooleanField
from foledol.django.tools.form import Form
from foledol.django.tools.handlers import confirm
from foledol.django.tools.table import Table, TableColumn
from foledol.django.utils import pop_path, get_path, get_param, error, paginate, new_context, print_report, delete_all, \
    get_integer


class RawSQLite(RawSQL):
    def as_sql(self, compiler, connection):
        return '%s' % self.sql, self.params

    def get_group_by_cols(self):
        return [self]


class GridForm(Form):
    def __init__(self, context):
        super().__init__(context, [
            TextField('name', "Nom", min_length=1),
            TextField('table', "Table"),
            TextField('comment', "Description"),
            TextField('filter_by', "Filtre"),
            BooleanField('group_by', "Regrouper"),
            BooleanField('distinct', "Valeurs distinctes"),
            BooleanField('show_on_home', "Afficher sur la page d'accueil"),
        ])


class ColumnSubTable(Table):
    def __init__(self, rows, read_only=False):
        super().__init__(rows, [
            TableColumn('label', "Libellé", method='label_as_str'),
            TableColumn('order', "Ordre")
        ])
        self.heading = 'Colonnes'
        self.update = 'django:column_update' if not read_only else None
        self.create = 'django:column_create' if not read_only else None
        self.placeholder = "Ajouter une colonne"


UPDATE_ACTIONS = [
    'condition_group_add_0',
    'condition_group_add_1',
    'condition_group_switch',
    'condition_group_delete',
    'condition_group_move_up',
    'condition_group_move_dw',
    'condition_move_up',
    'condition_move_dw'
]


def grid_get_filter(code, grid_filters):
    if code == '(none)':
        return None
    for grid_filter in grid_filters:
        if grid_filter.code == code:
            return grid_filter
    return None


def grid_form(request, grid, read_only=False):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    action = get_path(request, context, grid, 'grid', space='django')
    if action == 'clone':
        grid = grid.clone()
        request.session['path'] = request.POST['path']
        return HttpResponseRedirect(reverse('django:grid_update', kwargs={'pk': grid.id}) + '?back')

    context['read_only'] = read_only

    edit_as_str = get_param(request, context, 'edit', 'False')
    edit = edit_as_str != 'False'

    if grid:
        context['grid'] = grid
    context['grid_url'] = reverse('django:grid_update', kwargs={'pk': grid.id}) if grid else None

    form = GridForm(context)
    form.read(request.POST if action else {}, grid)
    if action == 'update':
        # TODO: fix the issue on BooleanField (Read)
        form.field('distinct').value = 'distinct' in request.POST
        form.field('group_by').value = 'group_by' in request.POST
        form.field('show_on_home').value = 'show_on_home' in request.POST

    if len(action) > 0:
        form.validate()

    context['tables'] = settings.GRID_TABLES
    context['table'] = grid.table if grid else 'member'

    columns = grid.column_set.all().order_by('order') if grid else None
    context['columns'] = columns
    context['table_columns'] = ColumnSubTable(columns, read_only=not request.user.is_staff)

    grid_table = settings.GRID_TABLES[grid.table] if grid and grid.table in settings.GRID_TABLES else None

    grid_filter = grid.filter if grid and grid.filter else '(none)'
    grid_filter = get_param(request, context, 'filter', grid_filter)
    if grid:
        grid.filter = grid_filter

    grid_filters = grid_table.filters if grid_table else []
    context['grid_filters'] = grid_filters

    if grid and not grid.group_by:
        if grid_table and len(grid_table.reports) > 0:
            context['reports'] = grid_table.reports

    fields = grid_table.fields if grid_table else None
    context['fields'] = fields

    if edit:
        update_values(request, grid, grid_table, columns, fields)

    if action == 'edit':
        edit = True
    if action == 'done':
        edit = False
    context['edit'] = edit

    grid_filter = grid_get_filter(grid_filter, grid_filters)

    objects = get_objects(grid, grid_table, grid_filter, context) if grid else None

    context['update'] = settings.DEFAULT_SPACE + ':' + grid.table + '_update' if grid else None

    condition = None
    condition_id = get_integer(request, 'condition_id', 0)
    if condition_id > 0:
        condition = Condition.objects.get(id=condition_id)
    condition_group = grid.condition_group if grid else None
    condition_group_id = get_integer(request, 'condition_group_id', 0)
    if condition_group_id > 0:
        condition_group = ConditionGroup.objects.get(id=condition_group_id)

    if action == 'condition_group_add_0' and condition_group:
        grid_condition_group_add(condition_group, 0)
    if action == 'condition_group_add_1' and condition_group:
        grid_condition_group_add(condition_group, 1)
    if action == 'condition_group_switch' and condition_group:
        condition_group.type = 1 if condition_group.type == 0 else 0
        condition_group.save()
    if action == 'condition_group_delete' and condition_group:
        grid_condition_group_delete(condition_group)
    if action == 'condition_group_move_up' and condition_group:
        grid_condition_group_move(condition_group, -15)
    if action == 'condition_group_move_dw' and condition_group:
        grid_condition_group_move(condition_group, +15)

    if action == 'condition_move_up' and condition:
        grid_condition_move(condition, -15)
    if action == 'condition_move_dw' and condition:
        grid_condition_move(condition, +15)

    if grid and grid.condition_group == condition_group:
        grid.condition_group = condition_group
    context['condition_group'] = grid.condition_group if grid else None
    context['condition_as_str'] = grid.condition_group.as_str() if grid else None

    try:
        rows = grid_rows(grid, objects, fields) if objects else None
    except Exception as ex:
        context['error'] = str(ex)
        rows = None

    if columns:

        default_sort = None
        for column in columns:
            if not column.hidden:
                default_sort = column.label + "_asc"
                break
        full_name = "grid_" + str(grid.id) + ".sort"
        default_sort = request.session[full_name] if full_name in request.session else default_sort

        path = request.POST['path'] if 'path' in request.POST else None
        sort = get_param(request, context, 'sort', default_sort) if path != ':/django/grids' else default_sort
        if 'sort' in request.GET:
            sort = request.GET['sort']

        request.session[full_name] = context['sort'] = sort

        if sort:
            if sort.endswith("_asc"):
                sort = sort[0:-4]
            if sort.endswith("_desc"):
                sort = "-" + sort[0:-5]
            if rows:
                rows = rows.order_by(sort)

    if 'copy' in request.GET:
        data = grid_copy(grid, rows, fields)
        return HttpResponse(data, 'application/json')

    if action == 'export':
        return grid_export(grid, rows, fields)

    if action == 'print' and grid:
        title = grid.comment if grid.comment else grid.name
        report = GridReport(title, grid, fields).build(rows)
        return print_report(report, grid.table + ".pdf")

    if action.startswith('print_') and grid and grid_table:
        key = action[6:]
        for report_item in grid_table.reports:
            if report_item.key == key and report_item.report:
                report = report_item.report
                output = report.output if hasattr(report, 'output') else grid.table + ".pdf"
                return print_report(report.build(rows), output)

    context['rows'] = paginate(request, context, rows) if rows else None
    context['count'] = rows.count() if rows else 0

    context['group_by'] = grid.group_by if grid else None
    context['group_by_url'] = grid_table.url if grid_table else None

    if context['error']:
        context['error_message'] = "Veuillez corriger les erreurs ci-dessous"
    if not action or context['error']:
        context['action'] = 'update' if grid else 'create'
        return render(request, 'grid.html', context)

    if action == 'create':
        grid = Grid()
    form.save_and_log(grid, 'grid', action, request)

    if not grid.condition_group:
        condition_group = ConditionGroup()
        condition_group.save()
        grid.condition_group = condition_group
        grid.save()

    if action == 'update' or action == 'edit' or action == 'done' or action in UPDATE_ACTIONS:
        context['action'] = 'update'
        return render(request, 'grid.html', context)
    return HttpResponseRedirect(context['back'] + '?path=' + pop_path(request))


@login_required
def grid_create(request):
    return grid_form(request, None)


@login_required
def grid_update(request, pk):
    grid = Grid.objects.filter(id=pk).first()
    return grid_form(request, grid) if grid else error(request)


@login_required
def grid_delete(request, pk):

    def prepare(context):
        grid = Grid.objects.get(id=pk)
        context['title'] = _('delete_grid_title').format(grid)
        context['cancel'] = reverse('django:grid_update', kwargs={'pk': pk})
        context['message'] = _('delete_grid_message').format(grid)
        return grid

    def execute(grid):
        delete_all(grid.column_set.all())
        grid.delete()

    return confirm(request, 'delete', prepare, execute, reverse('django:grids'))


@login_required
def grid_view(request, pk):
    grid = Grid.objects.filter(id=pk).first()
    return grid_form(request, grid, True) if grid else error(request)


def get_objects_from_manager(grid, context, manager, table, grid_filter):
    if grid.filter_by:
        try:
            sql = "SELECT id FROM {table} WHERE {filter_by}".format(table=table, filter_by=grid.filter_by)
            raw_sql = RawSQLite(sql, ()) if settings.CREATE_INSCRIPTION else RawSQL(sql, ())
            return manager.filter(id__in=raw_sql)
        except Exception as ex:
            context['warning'] = ex
    objects = manager.all()
    return grid_filter.filter(objects) if grid_filter else objects


def get_objects(grid, grid_table, grid_filter, context):
    return get_objects_from_manager(grid, context, grid_table.manager, grid_table.table, grid_filter)


def grid_condition_group_add(condition_group, type):
    condition_groups = ConditionGroup.objects.filter(condition_group=condition_group)
    new_condition_group = ConditionGroup(condition_group=condition_group, type=type)
    new_condition_group.order = (condition_groups.count() + 1) * 10
    new_condition_group.save()


def grid_condition_group_delete(condition_group):
    parent = condition_group.condition_group
    delete_all(condition_group.condition_set.all())
    condition_group.delete()
    grid_condition_group_renumber(parent)


def grid_condition_move(condition, delta):
    condition.order += delta
    condition.save()
    grid_condition_group_renumber(condition.condition_group)


def grid_condition_group_move(condition_group, delta):
    condition_group.order += delta
    condition_group.save()
    grid_condition_group_renumber(condition_group.condition_group)


def grid_condition_group_renumber(condition_group):
    order = 10
    for child in condition_group.children():
        if child.order != order:
            if child.condition_group:
                child.condition_group.order = order
                child.condition_group.save()
            elif child.condition:
                child.condition.order = order
                child.condition.save()
        order += 10


def grid_rows(grid, rows, fields):
    for column in grid.column_set.all():
        field = get_field(column.label, fields)
        if field and field.external:
            rows = rows.annotate(**{field.key: F(field.key)})

    if grid.condition_group:
        rows = rows.filter(grid.condition_group.get_filter())

    if grid.group_by:
        values = []
        for column in grid.column_set.all():
            field = get_field(column.label, fields)
            if field and not column.hidden:
                values.append(field.key)
        rows = rows.values(*values)

    return rows.distinct() if grid.distinct else rows


def get_field(key, fields):
    for field in fields:
        if field.key == key:
            return field
    return None


def update_values(request, grid, grid_table, columns, fields):
    ids = []

    for key in request.POST.keys():
        if key.startswith('row_'):
            ids.append(int(key[4:]))

    for id in ids:
        values = {}
        for column in columns:
            new_key = str(id) + '_' + column.label
            old_key = new_key + '_old'

            field = get_field(column.label, fields)
            default = 'False' if field and isinstance(field, BooleanField) else None

            old = request.POST[old_key] if old_key in request.POST else default
            new = request.POST[new_key] if new_key in request.POST else default
            if new != old:
                values[column.label] = new
        if len(values.keys()) > 0:
            update(request, grid, grid_table.manager.filter(id=id).first(), values, fields)


def update(request, grid, obj, values, fields=None):
    if obj is None:
        return
    updated = False
    old_values = {}
    new_values = {}
    for key in values.keys():
        field = get_field(key, fields)
        if field:
            field.set(values[key])
            if field.validate():
                updated |= update_value(obj, key, field.value, old_values, new_values)
        else:
            updated |= update_value(obj, key, values[key], old_values, new_values)
    if updated:
        obj.save()
        log(obj.id, grid.table, 'update', request.user, old_values, new_values)


def update_value(obj, key, value, old_values, new_values):
    new_value = value
    old_value = getattr(obj, key) if key in obj.__dict__ else value
    if old_value == new_value:
        return False
    setattr(obj, key, new_value)
    old_values[key] = old_value
    new_values[key] = new_value
    return True


def get_value(grid, row, column):
    return row[column.label] if grid.group_by else value(row, column.label)


def grid_copy(grid, rows, fields):
    data = ""

    for column in grid.column_set.all().order_by('order'):
        field = get_field(column.label, fields)
        if field and not column.hidden:
            if len(data) > 0:
                data += "\t"
            data += field.label
    data += "\n"

    for row in rows:
        line = ""
        for column in grid.column_set.all():
            field = get_field(column.label, fields)
            if field and not column.hidden:
                if len(line) > 0:
                    line += "\t"
                line += str(get_value(grid, row, column))
        data += line
        data += "\n"
    return data


def grid_export(grid, rows, fields):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    column_header = workbook.add_format()
    column_header.set_bold(True)
    column_header.set_align('top')
    column_header.set_align('center')
    column_header.set_text_wrap(True)

    worksheet = workbook.add_worksheet(grid.table)
    worksheet.set_landscape()

    i = 0
    for column in grid.column_set.all().order_by('order'):
        field = get_field(column.label, fields)
        if field and not column.hidden:
            worksheet.write(0, i, field.label, column_header)
            if column.width and column.width > 0:
                worksheet.set_column(i, i, round(column.width / 10))
            i += 1

    j = 1
    for row in rows:
        i = 0
        for column in grid.column_set.all():
            field = get_field(column.label, fields)
            if field and not column.hidden:
                worksheet.write(j, i, get_value(grid, row, column))
                i += 1
        j += 1

    workbook.close()
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="' + grid.table + '.xlsx"'
    return response
