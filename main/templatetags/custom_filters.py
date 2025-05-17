from django import template

register = template.Library()

@register.filter(name='mul')
def mul(value, arg):
    """Multiply the arg by the value."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter(name='divide')
def divide(value, arg):
    """Divide the value by the arg."""
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
    
@register.filter(name='percentage')
def percentage(value, arg):
    """Calculate what percentage of arg is value."""
    try:
        return (int(value) / int(arg)) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
