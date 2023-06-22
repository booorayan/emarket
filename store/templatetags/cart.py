from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag
def cart(products):
    return products


@register.filter(name='is_in-cart')
def is_in_cart(product, ocart):
    keys = ocart.keys()
    for iid in keys:
        if int(iid) == product.id:
            return True
    return False


@register.filter(name='cart_quantity')
def cart_quantity(product, ocart):
    keys = ocart.keys()
    for iid in keys:
        if int(iid) == product.id:
            return ocart.get(iid)
    return 0


@register.filter
@stringfilter
def currency(value):
    return int(value)


@register.filter
@stringfilter
def is_in_cart(item, ocart):
    if item in ocart:
        return item
    else:
        return None


@register.filter
@stringfilter
def cart_quantity(item, ocart):
    return ocart.count(item)
