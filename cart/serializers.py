from rest_framework import serializers

from product.serializers import ProductSerializer
from .models import Cart


class CartSerializer(serializers.ModelSerializer):

    products = ProductSerializer()

    class Meta:
        model = Cart
        fields = (
            'products'
        )
