from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from foledol.django.tools.table import Table, TableColumn
from foledol.django.utils import get_search, paginate, new_context

from ..models import Column


class ConditionTables(Table):
    def __init__(self, rows):
        super().__init__(rows, [
            TableColumn('label', "Libellé"),
            TableColumn('criteria', "Critère"),
            TableColumn('value', "Valeur")
        ])
        self.update = 'django:condition_update'
        self.create = 'django:condition_create'
        self.search = True


@login_required
@staff_member_required
def condition_list(request):
    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    conditions = Column.objects.all()

    search = get_search(request).strip()
    if len(search) > 0:
        conditions = Column.objects.filter(label=search)
    context['search'] = search
    context['table'] = ConditionTables(paginate(request, context, conditions))

    return render(request, 'conditions.html', context)
