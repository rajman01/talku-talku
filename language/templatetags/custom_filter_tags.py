from django import template


register = template.Library()



@register.filter
def capitalize_all(value):
    return value.upper()


@register.filter
def shrink(value):
    if len(value) < 100:
        return value
    return value[:99]


@register.filter
def get_index(item, lst):
    return lst.index(item)


@register.filter
def multiply(value):
    value = int(value)
    return str(value * 100)