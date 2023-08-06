import datetime
import os

import matplotlib.pyplot as plt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden, FileResponse
from django.shortcuts import render
from django.urls import reverse

from foledol.django.tools.table import Table, TableColumn, TableButton
from foledol.django.utils import get_param, paginate, get_param_from_request, new_context, can_navigate, navigate, \
    get_path
from foledol.django.utils import remove_file, get_color, get_local_date
from ..models import Log


class LogTable(Table):
    def __init__(self, rows):
        super().__init__(rows, [
            TableColumn('date', "Date", sortable=True, method='date_as_str'),
            TableColumn('user', "Utilisateur"),
            TableColumn('model', "Table"),
            TableColumn('action', "Action")
        ])
        self.update = 'django:log_update'
        self.buttons = [
            TableButton("Calculer", "send('compute')"),
        ]
        self.search = True


def get_logs(request, context):
    logs = Log.objects.all()

    search = get_param_from_request(request, context, 'logs', 'search', '').strip()
    if len(search) > 0:
        logs = logs.filter(
            Q(user__email__icontains=search) |
            Q(user__username__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(model__icontains=search) |
            Q(action__icontains=search)
        )
    context['search'] = search

    sort = get_param(request, context, 'sort', 'date_desc')
    return logs.order_by('date' if sort == 'date_asc' else '-date')


@login_required
def log_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    logs = get_logs(request, context)

    context['table'] = LogTable(paginate(request, context, logs, space='logs'))

    return render(request, 'logs.html', context)


@login_required
def log_events(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    log_draw_plot()
    log_draw_plot_today()

    plots = ['plot', 'plot_today']
    for plot in plots:
        if log_has_plot('log_{}.png'.format(plot)):
            context[plot] = reverse('django:log_{}'.format(plot))

    return render(request, 'log_events.html', context)


@login_required
def log_update(request, pk):
    log = Log.objects.get(id=pk)

    context = new_context()
    context['base'] = settings.DEFAULT_SPACE + '/base.html'

    get_path(request, context, log, 'log', space='django')

    context['log'] = log
    context['log_items'] = log.items.all()

    context['navigate'] = can_navigate(request, context, '/logs') and log
    if context['navigate']:
        logs = get_logs(request, context)
        navigate(request, context, logs, log.id)

    return render(request, 'log.html', context)


@login_required
def log_plot(request):
    return log_get_plot('log_plot.png')


@login_required
def log_plot_today(request):
    return log_get_plot('log_plot_today.png')


def log_has_plot(name):
    path = os.path.join(settings.MEDIA_ROOT, name)
    return os.path.isfile(path)


def log_get_plot(name):
    path = os.path.join(settings.MEDIA_ROOT, name)
    if log_has_plot:
        return FileResponse(open(path, 'rb'))
    return HttpResponseForbidden()


def log_draw_plot():
    path = os.path.join(settings.MEDIA_ROOT, 'log_plot.png')
    remove_file(path)

    values = [0] * 24 * 6 * 3

    x = []
    y = []

    now = get_local_date() - datetime.timedelta(3)
    for log in Log.objects.filter(date__gte=now).order_by('date'):
        delta = log.date - now
        key = int((delta.days * (24 * 6)) + (delta.seconds / 600))
        if values[key] < 100:
            values[key] += 1

    mx = 0
    dt = now
    for value in values:
        x.append(dt)
        y.append(value)
        if value > mx:
            mx = value
        dt += datetime.timedelta(minutes=10)

    plt.xlim(now, now+datetime.timedelta(3))

    plt.title("Les 3 derniers jours")
    plt.ylim(0, mx + 5)
    plt.plot(x, y, color=get_color("9398C2FF"))
    plt.savefig(path, dpi=400)
    plt.clf()


def log_draw_plot_today():
    path = os.path.join(settings.MEDIA_ROOT, 'log_plot_today.png')
    remove_file(path)

    values = [0] * 8 * 6

    x = []
    y = []

    now = get_local_date() - datetime.timedelta(seconds=8*60*60)
    for log in Log.objects.filter(date__gte=now).order_by('date'):
        delta = log.date - now
        key = int((delta.seconds / 600))
        if values[key] < 100:
            values[key] += 1

    mx = 0
    dt = now
    for value in values:
        x.append(dt)
        y.append(value)
        if value > mx:
            mx = value
        dt += datetime.timedelta(minutes=10)

    plt.xlim(now, now + datetime.timedelta(seconds=8*60*60))

    plt.title("Les 8 dernières heures")
    plt.ylim(0, mx + 5)
    plt.plot(x, y, color=get_color("9398C2FF"))
    plt.gcf().autofmt_xdate()
    plt.savefig(path, dpi=400)
    plt.clf()
