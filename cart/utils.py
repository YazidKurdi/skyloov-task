from .models import CartItem

def product_in_cart(cart,product):
    return CartItem.objects.filter(cart=cart,product=product)
