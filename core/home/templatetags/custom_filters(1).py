from django import template

register = template.Library()

@register.filter
def starts_with(value, arg):
    """Check if a string starts with a specific prefix."""
    return value.startswith(arg)