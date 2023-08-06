from django import template
from django.urls import reverse

from foledol.django.tools.form import Form

register = template.Library()


translatable = {
    'table.search': "Rechercher"
}


@register.filter
def translate(label):
    return translatable[label]


@register.filter
def get(obj, column):
    try:
        if column.value:
            return value(obj, column.value)
        return value(obj, column.key)
    except AttributeError:
        return None


@register.filter
def value(obj, name):
    split = name.split('.', 1)
    if len(split) > 1:
        return value(getattr(obj, split[0]), split[1])
    return getattr(obj, name) if obj else None


@register.filter
def method(obj, name):
    split = name.split('.', 1)
    if len(split) > 1:
        return method(getattr(obj, split[0]), split[1])
    return getattr(obj, name)() if obj else None


@register.filter
def formatter(table, row):
    return table.formatter(row)


@register.filter
def field(form, key):
    return form.field(key)


@register.filter
def query(dictionary):
    query_str = ''
    for key in dictionary.keys():
        if len(query_str) > 0:
            query_str += "&"
        query_str += key + "=" + str(dictionary[key])
    return query_str


@register.filter
def report(reports, key):
    return reports[key]


@register.filter
def editor(row, fields):
    return Form(context={}, fields=fields)


@register.filter
def class_name(obj):
    return type(obj).__name__


links = {}


@register.filter
def link(obj, name):
    return links[name](obj)


def register_link(name):
    def register_link_inner(function):
        links[name] = function
    return register_link_inner


@register.filter
def resolve(name, pk):
    return reverse(name, kwargs={'pk': pk}) if pk > 0 else None
