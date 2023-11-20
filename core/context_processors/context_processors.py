from core.models import *


def settings(request):
    cart_products = CartProduct.objects.all()
    sum_ = 0

    if cart_products:
        sum_ = sum(cart_product.product.price * cart_product.quantity for cart_product in cart_products)


    context = {
        'footer_info': Settings.objects.first(),
        'logo': Logo.objects.first(),
        'cart_products': cart_products,
        'sum_': round(sum_, 2),
        'cart_products_count': cart_products.count()
    }
    
    return context