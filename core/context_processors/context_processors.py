from django.db.models import Q
from core.models import *


def settings(request):
    cart_products = CartProduct.objects.filter(active=True)
    sum_ = 0

    if cart_products:
        sum_ = sum(cart_product.product.price * cart_product.quantity for cart_product in cart_products)


    context = {
        'footer_info': Settings.objects.first(),
        'logo': Logo.objects.first(),
        'cart_products': cart_products,
        'sum_': round(sum_, 2) if sum_ != 0 else 0,
        'cart_products_count': cart_products.count(),
        'whish_list_count': Clothes.objects.filter(Q(added_to_whishlist=True) & Q(active=True)).count(),
    }
    
    return context