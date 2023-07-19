from rest_framework import serializers

from product.serializers import ProductSerializer
from .models import Cart, CartItem


from rest_framework import serializers
from .models import Cart, CartItem
from product.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    sub_total = serializers.SerializerMethodField()
    quantity = serializers.ReadOnlyField()
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'sub_total')

    def get_sub_total(self, obj):
        return obj.subTotal

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    num_of_items = serializers.SerializerMethodField()
    cart_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'owner', 'created_at', 'num_of_items', 'cart_total', 'cart_items')

    def get_num_of_items(self, obj):
        return obj.num_of_items

    def get_cart_total(self, obj):
        return obj.cart_total