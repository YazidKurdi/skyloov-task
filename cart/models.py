from django.db import models
from django.contrib.auth import get_user_model

from product.models import Product

User = get_user_model()

class Cart(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, related_name='carts')

    def __str__(self):
        return f"{self.user.username}'s Cart"

