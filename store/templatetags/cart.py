from django import template


register = template.Library()


@register.filter(name='is_in_cart')
def is_in_cart(product, ocart):
    keys = ocart.keys()
    # for iid in keys:
    #     if int(iid) == product.id:
    #         return True
    # return False
    for item in keys:
        if item == product:
            return True
    return False


@register.filter(name='cart_quantity')
def cart_quantity(product, ocart):
    keys = ocart.keys()
    # for iid in keys:
    #     if int(iid) == product.id:
    #         return ocart.get(iid)
    # return 0

    for item in keys:
        if item == product:
            return ocart.get(item)
    return 0

