from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def version():
    return settings.VERSION


@register.simple_tag
def custom_company():
    return settings.CUSTOM_COMPANY


@register.simple_tag
def custom_address():
    return settings.CUSTOM_ADDRESS


@register.simple_tag
def appointments():
    return settings.APPOINTMENTS


@register.simple_tag
def time_slots():
    return settings.TIME_SLOTS


@register.filter
def setting(label):
    try:
        return getattr(settings, label)
    except AttributeError:
        return None


@register.filter
def member_of(user, group):
    return user.groups.filter(name=group).count() > 0

