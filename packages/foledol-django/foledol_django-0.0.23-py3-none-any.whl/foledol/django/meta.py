import io
from datetime import datetime

import xlsxwriter
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.timezone import make_aware
from django.db import models

from foledol.django.utils import to_float

FORMAT_CHAR = 0
FORMAT_TEXT = 1
FORMAT_DATE = 2
FORMAT_BOOLEAN = 3
FORMAT_INTEGER = 4
FORMAT_FLOAT = 5


class ModelField:
    def __init__(self, column, name, label, format=FORMAT_CHAR, values=None, mandatory=True):
        self.column = column
        self.name = name
        self.label = label
        self.format = format
        self.values = values
        self.mandatory = mandatory


def check_headers(fields, row):
    for field in fields:
        if field.column >= len(row) or not field.mandatory:
            continue
        cell = row[field.column]
        value = cell.value
        if value != field.label:
            raise Exception('Invalid header', value + '<>' + field.label)


def read_fields(fields, row):
    values = {}
    for field in fields:
        if field.column >= len(row):
            continue
        cell = row[field.column]
        value = cell.value
        if field.format == FORMAT_DATE:
            values[field.name] = make_aware(value) if value else None
        elif field.format == FORMAT_BOOLEAN:
            values[field.name] = len(value) > 0 if value else False
        elif field.format == FORMAT_INTEGER:
            values[field.name] = int(value) if value else None
        elif field.format == FORMAT_FLOAT:
            values[field.name] = to_float(value) if value else None
        else:
            values[field.name] = value if value else ""
    return values


def get_field(name, fields):
    for field in fields:
        if field.name == name:
            return field
    return None


def get_fields(item, fields):
    values = {}
    for field in fields:
        values[field.name] = getattr(item, field.name)
    return values


def set_fields(item, values):
    for key in values.keys():
        setattr(item, key, values[key])


def copy_fields(items, fields):
    data = ""
    for field in fields:
        if len(data) > 0:
            data += "\t"
        data += field.label
    data += "\n"

    for item in items:
        values = get_fields(item, fields)
        line = ""
        for key in values.keys():
            if len(line) > 0:
                line += "\t"
            line += str(values[key])
        data += line
        data += "\n"
    return data


def write_headers(fields, worksheet, row, format):
    i = 0
    for field in fields:
        worksheet.write(row, i, field.label, format)
        i += 1


def write_values(fields, values, worksheet, row, format=None):
    i = 0
    for field in fields:
        value = values[field.name]
        if field.format == FORMAT_BOOLEAN and field.values and value in field.values:
            value = field.values[value]
        if format:
            worksheet.write(row, i, value, format)
        else:
            worksheet.write(row, i, value)
        i += 1


def export_to_worksheet(workbook, items, fields, title):
    format_header = workbook.add_format()
    format_header.set_bold(True)
    format_header.set_align('top')
    format_header.set_align('center')
    format_header.set_text_wrap(True)

    worksheet = workbook.add_worksheet(title)
    worksheet.set_landscape()

    write_headers(fields, worksheet, 0, format_header)
    row = 1
    for item in items:
        values = get_fields(item, fields)
        write_values(fields, values, worksheet, row)
        row += 1

    workbook.close()


def export_to_workbook_buffer(items, fields, title):
    output = io.BytesIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    export_to_worksheet(workbook, items, fields, title)

    output.seek(0)
    return output


def export_to_workbook(items, fields, filename, title):
    output = export_to_workbook_buffer(items, fields, title)
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
    return response


def get_new_field(key, fields):
    for field in fields:
        if field.key == key:
            return field
    return None

#
# Metadata
#


def meta_user(related_name):
    return models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None, null=True, related_name=related_name)


def creator(model):
    return meta_user(model + "_creator")


def updator(model):
    return meta_user(model + "_updator")


def set_meta(action, user, item):
    user = get_user_or_superuser(user)
    if action == 'create':
        item.created_by = user
        item.created_at = datetime.now()
    else:
        item.updated_by = user
        item.updated_at = datetime.now()


def get_user_or_superuser(user):
    return User.objects.filter(is_superuser=True).first() if user.is_anonymous else user
