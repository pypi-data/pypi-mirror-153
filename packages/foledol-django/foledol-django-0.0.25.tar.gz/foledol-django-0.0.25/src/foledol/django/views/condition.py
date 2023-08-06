from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

from foledol.django.logger import log
from foledol.django.tools.field import TextField, IntegerField, BooleanField, DateField, FloatField
from foledol.django.tools.form import Form
from foledol.django.tools.handlers import confirm
from foledol.django.utils import pop_path, get_path, get_param, get_integer, error, new_context
from .grid import get_field
from ..models import CRITERIA_SET, TEXT_CRITERIA_SET, DATE_CRITERIA_SET, \
    NUMBER_CRITERIA_SET, BOOLEAN_CRITERIA_SET, Condition, ConditionGroup


class ConditionForm(Form):
    def __init__(self, context):
        super().__init__(context, [
            TextField('label', "Libellé", min_length=1),
            IntegerField('criteria', "Critère"),
            TextField('value', "Valeur")
        ])


def condition_form(request, condition):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    action = get_path(request, context, condition, 'condition', space='django')

    condition_group_id = get_integer(request, 'condition_group_id', 0)
    if condition_group_id > 0:
        condition_group = ConditionGroup.objects.all().get(id=condition_group_id)
    elif condition:
        condition_group = condition.condition_group
    context['condition_group_id'] = condition_group.id

    if condition:
        context['condition'] = condition

    grid = condition_group.grid() if condition_group else None
    fields = grid.fields() if condition_group else []
    context['fields'] = fields

    context['criteria_set'] = CRITERIA_SET

    form = ConditionForm(context)
    form.read(request.POST, condition)

    order = (condition_group.condition_set.count() + 1) * 10 if condition_group else 10

    criteria = get_integer(request, 'criteria', condition.criteria if condition else 0)
    context['criteria'] = criteria

    if len(action) > 0:
        form.validate()

    if context['error']:
        context['error'] = "Veuillez corriger les erreurs ci-dessous"

    label = get_param(request, context, 'label', None)
    if label and condition:
        field = get_field(condition.label, fields)
        if isinstance(field, TextField):
            if criteria not in TEXT_CRITERIA_SET:
                context['error'] = "Le critère n'est pas compatible avec un texte"
        if isinstance(field, DateField):
            if criteria not in DATE_CRITERIA_SET:
                context['error'] = "Le critère n'est pas compatible avec une date"
        if isinstance(field, FloatField) or isinstance(field, IntegerField):
            if criteria not in NUMBER_CRITERIA_SET:
                context['error'] = "Le critère n'est pas compatible avec un nombre"
        if isinstance(field, BooleanField):
            if criteria not in BOOLEAN_CRITERIA_SET:
                context['error'] = "Le critère n'est pas compatible avec un booléen"

    if not action or context['error']:
        context['action'] = 'update' if condition else 'create'
        return render(request, 'condition.html', context)

    if action == 'create':
        condition = Condition(condition_group=condition_group)
    form.save(condition)
    if not condition.order:
        condition.order = order
    condition.save()
    #if condition_group:
    #    condition_group_renumber(condition_group)
    log(condition.id, 'condition', action, request.user, form.old_values, form.new_values)

    return HttpResponseRedirect(context['back'] + '?path=' + pop_path(request))


@login_required
def condition_create(request):
    return condition_form(request, None)


@login_required
def condition_update(request, pk):
    condition = Condition.objects.filter(id=pk).first()
    return condition_form(request, condition) if condition else error(request)


@login_required
def condition_delete(request, pk):
    def prepare(context):
        condition = Condition.objects.get(id=pk)
        context['title'] = _('delete_condition_title').format(condition)
        context['cancel'] = reverse('django:condition_update', kwargs={'pk': pk})
        context['message'] = _('delete_condition_message').format(condition)
        return condition

    def execute(condition):
        condition.delete()

    return confirm(request, 'delete', prepare, execute, reverse('django:conditions'))
