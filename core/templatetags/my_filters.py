from django import template
from core.models import Clothes


register = template.Library()

@register.simple_tag
def get_products(offset, limit, down_up):
    if down_up == 1:
        return Clothes.objects.filter(active=True).order_by('-update_time')[offset:limit]
    return Clothes.objects.filter(active=True).order_by('update_time')[offset:limit]


@register.filter
def filter_(any_string: str):
    return any_string.upper()


@register.filter
def multiply_(price, quantity):
    return price * quantity

