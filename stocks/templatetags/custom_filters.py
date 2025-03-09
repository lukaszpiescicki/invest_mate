from django import template

register = template.Library()


@register.filter
def billions(value):
    try:
        value_in_billions = value / 1_000_000_000
        return f"${value_in_billions:.2f}B"
    except (TypeError, ValueError):
        return value
