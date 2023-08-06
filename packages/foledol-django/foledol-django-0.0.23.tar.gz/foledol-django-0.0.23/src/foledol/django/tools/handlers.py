from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render

from ..utils import pop_path, get_param


def confirm(request, action, prepare, execute, back, space=settings.DEFAULT_SPACE, is_staff=False):
    if not request.user.is_staff and not is_staff:
        return HttpResponseForbidden()
    context = {'error': None, 'base': space + '/base.html' if space else 'base.html'}
    get_param(request, context, 'path', '')
    back = get_param(request, context, 'back', back)
    obj = prepare(context)
    if action not in request.POST:
        return render(request, 'common/' + action + '.html', context)
    execute(obj)
    return HttpResponseRedirect(back + '?path=' + pop_path(request))


def confirm_delete(request, action, prepare, back):

    def delete_object(obj):
        obj.delete()

    return confirm(request, action, prepare, delete_object, back)
