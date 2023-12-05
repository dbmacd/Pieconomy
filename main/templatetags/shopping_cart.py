from django import template
from main.models import OrderItems, Orders

register = template.Library()


@register.simple_tag
def cart_count(user_id):
    user_order = Orders.objects.filter(is_ordered=False, user_id=user_id).first()
    try:
        order_items = OrderItems.objects.filter(order_id=user_order.id)
        total_qty = sum([item.quantity for item in order_items])
    except AttributeError:
        return ""
    return total_qty


@register.simple_tag
def tax(sub_total):
    return f'{round(float(sub_total) * float(0.1), 2):.2f}'


@register.simple_tag
def grand_total(sub_total):
    return f'{round(float(sub_total) * float(1.1), 2):.2f}'
