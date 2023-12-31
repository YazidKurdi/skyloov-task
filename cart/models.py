from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from product.models import Product

User = get_user_model()


class Cart(models.Model):

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def num_of_items(self):
        """
        Calculate and return the total number of items in the cart.
        """
        cart_items = self.cart_items.all()
        qtysum = sum([qty.quantity for qty in cart_items])
        return qtysum

    @property
    def cart_total(self):
        """
        Calculate and return the total price of all items in the cart.
        """
        cart_items = self.cart_items.all()
        qtysum = sum([qty.subTotal for qty in cart_items])
        return qtysum

    @receiver(post_save, sender=User)
    def create_cart(sender, instance, created, **kwargs):
        """
        Create a cart for the user upon user creation.
        """
        if created:
            Cart.objects.create(owner=instance)

    def __str__(self):
        return str(self.owner)


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=1)

    @property
    def subTotal(self):
        """
        Calculate and return the subtotal for the cart item.
        """
        total = self.quantity * self.product.min_price
        return total

    class Meta:
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
