import pytz
from django import template
from ..utils import get_long_date, get_long_datetime

DAYS_OF_WEEK = ['Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa', 'Di']

register = template.Library()

tz = pytz.timezone("Europe/Brussels")


@register.filter
def weekday(value):
    return DAYS_OF_WEEK[value.weekday()]


@register.filter
def long_date(value):
    return get_long_date(value)


@register.filter
def long_datetime(value):
    return get_long_datetime(value)


@register.filter
def short_datetime(value):
    return value.astimezone(tz).strftime('%d/%m/%Y %H:%M')
