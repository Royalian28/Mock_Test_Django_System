from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(str(key))
    except:
        return None

@register.filter
def get_range(value):
    """Returns a range from 0 to value-1"""
    return range(value)
