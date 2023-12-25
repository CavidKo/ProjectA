from django import template
from core.models import Clothes
from datetime import datetime


month_mapping = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
    9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec',
}


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

@register.filter(name='full_star_range')
def get_full_star_range(value):
    return range(value)


@register.filter(name='empty_star_range')
def get_empty_star_range(value):
    return range(5 - value)


@register.filter(name='convert_datetime')
def get_datetime(value: datetime):
    return f'{month_mapping[value.month]} {value.day}, {value.year}'


tags = {
    'dəb': 'dəb',
    'həyat tərzi': 'həyat-tərzi',
    'küçə tərzi': 'küçə-tərzi',
    'sənətkarlıq': 'sənətkarlıq',
    'cins': 'cins',
    'fashion': 'fashion',
    'lifestyle': 'lifestyle',
    'denim': 'denim',
    'streetstyle': 'streetstyle',
    'crafts': 'crafts'
}

@register.filter(name='get_slugifyer')
def get_slugifyer(tag: str):
    return tags[tag]
