import pytz
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

CRITERIA_NONE = 0
CRITERIA_EQUAL = 1
CRITERIA_NOT_EQUAL = 2
CRITERIA_LESS_THAN = 3
CRITERIA_LESS_THAN_OR_EQUAL = 4
CRITERIA_GREATER_THAN = 5
CRITERIA_GREATER_THAN_OR_EQUAL = 6
CRITERIA_CONTAINS = 7
CRITERIA_STARTS_WITH = 8
CRITERIA_ENDS_WITH = 9
CRITERIA_TRUE = 10
CRITERIA_FALSE = 11
CRITERIA_NULL = 12
CRITERIA_NOT_NULL = 13

TEXT_CRITERIA_SET = [
    CRITERIA_NONE,
    CRITERIA_EQUAL,
    CRITERIA_NOT_EQUAL,
    CRITERIA_CONTAINS,
    CRITERIA_STARTS_WITH,
    CRITERIA_ENDS_WITH,
    CRITERIA_NULL,
    CRITERIA_NOT_NULL
]

DATE_CRITERIA_SET = [
    CRITERIA_NONE,
    CRITERIA_EQUAL,
    CRITERIA_NOT_EQUAL,
    CRITERIA_CONTAINS,
    CRITERIA_STARTS_WITH,
    CRITERIA_ENDS_WITH,
    CRITERIA_NULL,
    CRITERIA_NOT_NULL
]

NUMBER_CRITERIA_SET = [
    CRITERIA_NONE,
    CRITERIA_EQUAL,
    CRITERIA_NOT_EQUAL,
    CRITERIA_LESS_THAN,
    CRITERIA_LESS_THAN_OR_EQUAL,
    CRITERIA_GREATER_THAN,
    CRITERIA_GREATER_THAN_OR_EQUAL,
    CRITERIA_NULL,
    CRITERIA_NOT_NULL
]

BOOLEAN_CRITERIA_SET = [
    CRITERIA_NONE,
    CRITERIA_TRUE,
    CRITERIA_FALSE
]

CRITERIA_SET = {
    #CRITERIA_NONE: "(aucun)",
    CRITERIA_EQUAL: "égal à",
    CRITERIA_NOT_EQUAL: "différent de",
    CRITERIA_LESS_THAN: "plus petit que",
    CRITERIA_LESS_THAN_OR_EQUAL: "plus petit ou égal",
    CRITERIA_GREATER_THAN: "plus grand que",
    CRITERIA_GREATER_THAN_OR_EQUAL: "plus grand ou égal",
    CRITERIA_CONTAINS: "contient",
    CRITERIA_STARTS_WITH: "commence par",
    CRITERIA_ENDS_WITH: "termine par",
    CRITERIA_TRUE: "vrai",
    CRITERIA_FALSE: "faux",
    CRITERIA_NULL: "vide",
    CRITERIA_NOT_NULL: "non vide",
}


class Log(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='actor')
    ref = models.CharField(max_length=64, default='')
    model = models.CharField(max_length=64, default='')
    date = models.DateTimeField(editable=True, null=True, blank=True)
    diff = models.TextField(default='')
    action = models.CharField(max_length=64, default='')
    transaction = models.CharField(max_length=64, default='', null=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.id)

    def author(self):
        return self.user.username if self.user else '(admin)'

    def date_as_str(self):
        tz = pytz.timezone('Europe/Paris')
        return self.date.astimezone(tz).strftime('%d/%m/%Y %H:%M')


class LogItem(models.Model):
    log = models.ForeignKey(Log, on_delete=models.DO_NOTHING, null=True, related_name='items')
    key = models.CharField(max_length=128, default='')
    old = models.CharField(max_length=128, default='', null=True)
    new = models.CharField(max_length=128, default='', null=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.id)


class GridTable:
    def __init__(self, label, fields, manager, table, url, reports=[], filters=[]):
        self.label = label
        self.fields = fields
        self.manager = manager
        self.table = table
        self.url = url
        self.reports = reports
        self.filters = filters


class ConditionChild:
    def __init__(self, order, condition=None, condition_group=None):
        self.order = order
        self.condition = condition
        self.condition_group = condition_group


class ConditionGroup(models.Model):
    condition_group = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    label = models.CharField(max_length=255, default='', null=True, blank=True)
    type = models.IntegerField(default=CRITERIA_EQUAL)
    order = models.IntegerField(default=0)

    objects = models.Manager()

    def clone(self, condition_group=None):
        condition_group = ConditionGroup(condition_group=condition_group)
        condition_group.label = self.label
        condition_group.type = self.type
        condition_group.order = self.order
        condition_group.save()

        old_condition_groups = ConditionGroup.objects.filter(condition_group=self)
        for old_condition_group in old_condition_groups:
            old_condition_group.clone(condition_group)

        old_conditions = Condition.objects.filter(condition_group=self)
        for old_condition in old_conditions:
            old_condition.clone(condition_group)

        return condition_group

    def __str__(self):
        return str(self.id)

    def type_as_str(self):
        return "ET (tous les critères)" if self.type == 0 else "OU (au moins un critère)"

    def as_str(self):
        expression = ''
        for child in self.children():
            if len(expression) > 0:
                if self.type == 0:
                    expression += ' ET '
                if self.type == 1:
                    expression += ' OU '
            if child.condition_group:
                expression += child.condition_group.as_str()
            if child.condition:
                expression += child.condition.as_str()
        return '(' + expression + ')'

    def grid(self):
        if self.condition_group:
            return self.condition_group.grid()
        return Grid.objects.filter(condition_group=self).first()

    def children(self):
        all_children = []
        condition_groups = ConditionGroup.objects.filter(condition_group=self)
        for condition_group in condition_groups:
            all_children.append(ConditionChild(condition_group.order, condition_group=condition_group))
        conditions = Condition.objects.filter(condition_group=self)
        for condition in conditions:
            all_children.append(ConditionChild(condition.order, condition=condition))
        return sorted(all_children, key=lambda child: child.order)

    def get_filter(self):
        try:
            filter_items = []
            for child in self.children():
                if child.condition:
                    filter_items.append(child.condition.get_filter())
                if child.condition_group:
                    filter_items.append(child.condition_group.get_filter())
            combined_filters = Q()
            for filter_item in filter_items:
                if combined_filters is None:
                    combined_filters = filter_item
                elif self.type == 0:
                    combined_filters &= filter_item
                elif self.type == 1:
                    combined_filters |= filter_item
            return combined_filters
        except Exception as ex:
            print("ERROR:" + str(ex))
        return None


class Grid(models.Model):
    name = models.CharField(max_length=255, default='', null=True, blank=True)
    table = models.CharField(max_length=255, default='', null=True, blank=True)
    filter = models.CharField(max_length=255, default='', null=True, blank=True)
    comment = models.CharField(max_length=255, default='', null=True, blank=True)
    filter_by = models.CharField(max_length=512, default='', null=True, blank=True)
    group_by = models.BooleanField(default=False)
    distinct = models.BooleanField(default=False)
    show_on_home = models.BooleanField(default=False)

    condition_group = models.ForeignKey(ConditionGroup, on_delete=models.DO_NOTHING, null=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.name)

    def table_as_str(self):
        return settings.GRID_TABLES[self.table].label if self.table in settings.GRID_TABLES else ''

    def fields(self):
        return settings.GRID_TABLES[self.table].fields if self.table in settings.GRID_TABLES else None

    def clone(self):
        grid = Grid()
        grid.name = self.name + "'"
        grid.table = self.table
        grid.filter = self.filter
        grid.comment = self.comment
        grid.filter_by = self.filter_by
        grid.group_by = self.group_by
        grid.distinct = self.distinct
        grid.show_on_home = self.show_on_home
        grid.condition_group = self.condition_group.clone()
        grid.save()

        for column in self.column_set.all():
            column.clone(grid)

        return grid


class Column(models.Model):
    grid: Grid = models.ForeignKey(Grid, on_delete=models.DO_NOTHING, null=True)

    label = models.CharField(max_length=255, default='', null=True, blank=True)
    value = models.CharField(max_length=255, default='', null=True, blank=True)
    criteria = models.IntegerField(default=CRITERIA_EQUAL)
    width = models.IntegerField(default=80, null=True, blank=True)
    order = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return str(self.id)

    def label_as_str(self):
        fields = self.grid.fields() if self.grid else None
        for field in fields:
            if field.key == self.label:
                return field.label
        return self.label

    def clone(self, grid):
        column = Column(grid=grid)
        column.label = self.label
        column.value = self.value
        column.criteria = self.criteria
        column.width = self.width
        column.order = self.order
        column.hidden = self.hidden
        column.save()
        return column


class Condition(models.Model):
    condition_group: ConditionGroup = models.ForeignKey(ConditionGroup, on_delete=models.DO_NOTHING, null=True)

    label = models.CharField(max_length=255, default='', null=True, blank=True)
    value = models.CharField(max_length=255, default='', null=True, blank=True)
    criteria = models.IntegerField(default=CRITERIA_EQUAL)
    order = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return str(self.id)

    def as_str(self):
        return self.label_as_str() + ' ' + self.criteria_as_str() + ' ' + self.value

    def label_as_str(self):
        grid = self.condition_group.grid() if self.condition_group else None
        fields = grid.fields() if grid else None
        for field in fields:
            if field.key == self.label:
                return field.label
        return self.label

    def label_with_operator(self, op):
        return str(self.label) + '__' + op

    def criteria_as_str(self):
        return CRITERIA_SET[self.criteria]

    def get_filter(self):
        try:
            if self.criteria == CRITERIA_NOT_EQUAL:
                return ~Q(**{self.label: self.value})
            elif self.criteria == CRITERIA_EQUAL:
                return Q(**{self.label: self.value})
            elif self.criteria == CRITERIA_LESS_THAN:
                return Q(**{self.label_with_operator('lt'): self.value})
            elif self.criteria == CRITERIA_LESS_THAN_OR_EQUAL:
                return Q(**{self.label_with_operator('lte'): self.value})
            elif self.criteria == CRITERIA_GREATER_THAN:
                return Q(**{self.label_with_operator('gt'): self.value})
            elif self.criteria == CRITERIA_GREATER_THAN_OR_EQUAL:
                return Q(**{self.label_with_operator('gte'): self.value})
            elif self.criteria == CRITERIA_CONTAINS:
                return Q(**{self.label_with_operator('contains'): self.value})
            elif self.criteria == CRITERIA_STARTS_WITH:
                return Q(**{self.label_with_operator('startswith'): self.value})
            elif self.criteria == CRITERIA_ENDS_WITH:
                return Q(**{self.label_with_operator('endswith'): self.value})
            elif self.criteria == CRITERIA_TRUE:
                return Q(**{self.label: True})
            elif self.criteria == CRITERIA_FALSE:
                return Q(**{self.label: False})
            elif self.criteria == CRITERIA_NULL:
                return Q(**{self.label_with_operator('isnull'): True})
            elif self.criteria == CRITERIA_NOT_NULL:
                return Q(**{self.label_with_operator('isnull'): False}) & ~Q(**{self.label_with_operator('exact'): ''})
        except Exception as ex:
            print("ERROR:" + str(ex))
        return None

    def clone(self, condition_group):
        condition = Condition(condition_group=condition_group)
        condition.label = self.label
        condition.value = self.value
        condition.criteria = self.criteria
        condition.order = self.order
        condition.save()
        return condition



