from datetime import datetime
from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()
@register.filter
@stringfilter
def str_to_date(value):
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')