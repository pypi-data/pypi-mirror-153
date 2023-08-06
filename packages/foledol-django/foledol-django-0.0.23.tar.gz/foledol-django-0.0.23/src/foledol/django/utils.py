# -*- coding: utf-8 -*-
import io
import os
import re
import shutil
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytz
from PIL import Image
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import LANGUAGE_SESSION_KEY


DAYS = [
    "Lun",
    "Mar",
    "Mer",
    "Jeu",
    "Ven",
    "Sam",
    "Dim",
]


def set_language(request, language):
    print(request.LANGUAGE_CODE)
    print(LANGUAGE_SESSION_KEY)
    if LANGUAGE_SESSION_KEY in request.session:
        print(request.session[LANGUAGE_SESSION_KEY])
    request.session[LANGUAGE_SESSION_KEY] = language


def new_context(extra=None):
    context = {'version': sys.version_info[0], 'error': None}
    return {**context, **extra} if extra else context


def to_float(value):
    value = value.replace('.', '')
    value = value.replace(',', '.')
    try:
        return float(value)
    except ValueError:
        return None


def find_id(item_id, items):
    for item in items:
        if item.id == item_id:
            return True
    return False


def get_ids(items):
    return [item.id for item in items]


def get_local_date():
    tz = pytz.timezone('Europe/Paris')
    return datetime.now(tz)


def get_date(request, label, default=None):
    try:
        if label in request.POST:
            return datetime.strptime(request.POST[label], '%d/%m/%Y')
        return default
    except ValueError:
        return default


def get_time(request, label, default=None):
    try:
        return datetime.strptime(request.POST[label], '%H:%M')
    except ValueError:
        return default


def get(value):
    return value if value else ''


def get_or(dictionary, label, value):
    return dictionary[label] if label in dictionary else value


def get_action(request):
    return get_or(request.POST, 'action', '')


def get_search(request):
    return get_or(request.POST, 'search', '')


def get_param(request, context, label, value):
    context[label] = get_or(request.POST, label, value)
    return context[label]


def get_param2(request, label, value):
    if label in request.GET:
        return request.GET[label]
    return get_param(request, label, value)


def get_filtered_items(request, context, space, items, filters):
    filter_key = get_param_from_request(request, context, space, 'filter_key', '')
    if filter_key and filter_key in filters:
        items = filters[filter_key].filter(items)
    return items


def get_param_from_request(request, context, space, label, value):
    full_name = space + "." + label
    if label in request.POST:
        context[label] = request.POST[label]
    else:
        context[label] = request.session[full_name] if full_name in request.session else value
    request.session[full_name] = context[label]
    return context[label]


def get_param_from_get_or_request(request, context, space, label, value):
    if label in request.GET:
        return request.GET[label]
    return get_param_from_request(request, context, space, label, value)


def get_boolean(request, context, label, value):
    context[label] = True if label in request.POST else value
    return context[label]


def get_integer(request, label, value=-1):
    try:
        return int(request.POST[label]) if label in request.POST else value
    except ValueError:
        return value


def get_integer2(request, label, value=-1):
    try:
        if label in request.GET:
            return int(request.GET[label]) if label in request.GET else value
        return get_integer(request, label, value)
    except ValueError:
        return value


def get_float(request, code, value=-1):
    if code in request.POST:
        return to_float(request.POST[code])
    return value


def get_long_date(date):
    return DAYS[date.weekday()] + " " + date.strftime('%d/%m/%Y')


def get_long_datetime(date):
    return DAYS[date.weekday()] + " " + date.strftime('%d/%m/%Y %H:%M')


def check_length(context, label, value):
    if len(value) < 1:
        context['error_on_' + label] = 'Ce champ est obligatoire'
        return False
    return True


def check_regex(context, label, value, pattern):
    matched = bool(re.search(pattern, value))
    if not matched:
        context['error_on_' + label] = "Ce champ n'est pas valide"
    return matched

#
# Navigation
#


can_navigate_params = ['sort', 'search']


def can_navigate(request, context, back):
    if context and 'back' in context and context['back'] != back:
        return False
    for param in can_navigate_params:
        if param not in request.POST:
            return False
    return True


def navigate(request, context, items, id):
    for param in can_navigate_params:
        get_param(request, context, param, '')

    if items.first():

        paginator_size = None
        if 'paginator_size' in request.POST and request.POST['paginator_size']:
            context['paginator_size'] = request.POST['paginator_size']
            paginator_size = int(context['paginator_size'])

        paginator_page = None
        if 'paginator_page' in request.POST and request.POST['paginator_page']:
            context['paginator_page'] = request.POST['paginator_page']
            paginator_page = int(context['paginator_page'])

        index = 0
        if paginator_page and paginator_size:
            size = (paginator_size * 3)
            index = ((paginator_page - 1) * paginator_size)
            page = int(index / size) + 1
            items = Paginator(items, size).page(page)
            index_prev = index
            index_next = index + paginator_size - 1
            index = ((page - 1) * size)

        item_index = -1
        prev_item = next_item = None
        for item in items:
            if item_index > -1:
                next_item = item
                break
            if item.id == id:
                item_index = index
                continue
            prev_item = item
            index += 1

        if prev_item:
            if paginator_page and paginator_size:
                context['prev_page'] = paginator_page - 1 if index - 1 < index_prev else paginator_page
            context['prev_id'] = prev_item.id
        if next_item:
            if paginator_page and paginator_size:
                context['next_page'] = paginator_page + 1 if index + 1 > index_next else paginator_page
            context['next_id'] = next_item.id

#
# Pagination
#


def paginate(request, context, results, length=15, space=None):

    paginate = request.session['paginate'] == 'on' if 'paginate' in request.session else False

    page = 1
    if 'paginator_page' in request.POST and request.POST['paginator_page']:
        page = int(request.POST['paginator_page'])
    elif space:
        full_name = space + '.page'
        page = request.session[full_name] if full_name in request.session else 1

    size = length
    if 'paginator_size' in request.POST and request.POST['paginator_size']:
        size = int(request.POST['paginator_size'])
    elif paginate:
        full_name = 'paginator_size'
        size = request.session[full_name] if full_name in request.session else length
    elif space:
        full_name = space + '.size'
        size = request.session[full_name] if full_name in request.session else length

    paginator = Paginator(results, size)

    last = paginator.num_pages
    if page > last:
        page = last

    context['pagination'] = last > 1
    context['page_count'] = results.count()
    context['page_init'] = 1
    context['page_prev'] = page - 1 if page > 1 else None
    context['page_next'] = page + 1 if page < last else None
    context['page_last'] = last
    context['paginator_page'] = page
    context['paginator_size'] = size

    if space:
        request.session[space + '.page'] = page
        request.session[space + '.size'] = size
    request.session['paginator_size'] = size

    return paginator.page(page)


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def send_mail2(to, subject, body):
    msg = MIMEMultipart()
    msg['From'] = settings.MAIL_USERNAME
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
    server.sendmail(settings.MAIL_USERNAME, to, msg.as_string())
    server.quit()


def print_report(pdf, filename):
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response


def has_diff(old, new):
    if old and new:
        for key in new.keys():
            if old[key] != new[key]:
                return True
    return False


def delete_all(items):
    for item in items:
        item.delete()


def remove_file(path):
    if path and os.path.isfile(path):
        os.remove(path)


def copy_file(source, target):
    remove_file(target)
    shutil.copyfile(source, target)


def push(items, item):
    if item in items:
        while items[-1] != item:
            items.pop()
        items.pop()


def get_back(request):
    path = get_path_from_request(request)
    return path.split(':')[-1]


def get_path_from_request(request):
    path = request.GET['path'] if 'path' in request.GET else None
    if path is None:
        path = get_param(request, {}, "path", "")
    return path


def get_path_leaf(request, context):
    path = get_path_from_request(request)
    action = get_action(request)
    if action == 'back':
        path = path.rsplit(':', 1)[0]
        action = ''
    context['back'] = path.split(':')[-1]
    context['path'] = path
    return action


def get_path(request, context, obj, prefix, space=settings.DEFAULT_SPACE):
    path = get_path_from_request(request)

    if 'back' in request.GET and 'path' in request.session:
        path = request.session['path']
        request.session.pop('path')
        path = path.rsplit(':', 1)[0]

    action = get_action(request)
    if action in ['back', 'open_item']:
        path = path.rsplit(':', 1)[0]
        action = ''
    else:
        if obj:
            item = reverse(space + ':' + prefix + "_update", kwargs={'pk': obj.id})
        else:
            item = reverse(space + ':' + prefix + "_create")
        items = path.split(":")
        push(items, item)
        items.append(item)
        path = ":".join(items)

    segments = path.split(':')
    context['back'] = segments[-2] if len(segments) > 1 else ''
    context['path'] = path
    context[prefix] = obj

    return action


def pop_path(request):
    path = request.POST['path'] if 'path' in request.POST else ''
    return path.rsplit(':', 1)[0]


def image_ratio(path):
    im = Image.open(path)
    return float(im.size[0]) / float(im.size[1])


def get_color(hex):
    return tuple(int(hex[i:i + 2], 16)/256.0 for i in (0, 2, 4, 6))


ERROR_404 = "Cet élément n'existe plus ..."


def error(request, message=ERROR_404):
    context = {'title': "Erreur", 'message': message}
    return render(request, 'common/error.html', context)


def write_field(output, value):
    output.write(value if value else '')
    output.write('\t')


#
# Logs
#


SEVERITY_INFO = 'info'
SEVERITY_ERROR = 'error'
SEVERITY_SUCCESS = 'success'


def log_message(message, severity, context=None):
    if context is not None:
        context[severity] = message
    print(severity.upper() + ":" + message)


def log_info(message, context=None):
    log_message(message, SEVERITY_INFO, context)


def log_error(message, context=None):
    log_message(message, SEVERITY_ERROR, context)


def log_success(message, context=None):
    log_message(message, SEVERITY_SUCCESS, context)


def split(items, size):
    rows = []
    row = None
    for item in items:
        if row and len(row) < size:
            row.append(item)
        else:
            row = [item]
            rows.append(row)
    return rows


def response_as_txt(output, title):
    response = HttpResponse(
        output.getvalue().encode("cp1252"),
        #output.getvalue().encode("iso-8859-1"),
        content_type='text/plain'
    )
    response['Content-Disposition'] = 'attachment; filename="' + title + '.txt"'
    return response


def to_file(output, path):
    if isinstance(output, io.StringIO):
        with open(path, mode='w') as file:
            output.seek(0)
            file.write(output.getvalue())
        return
    with open(path, mode='wb') as file:
        output.seek(0)
        shutil.copyfileobj(output, file, length=4096)
