from django import template

register = template.Library()

@register.filter
def uuid_lower(value):
    return str(value).lower()
