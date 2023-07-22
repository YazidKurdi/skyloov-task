from rest_framework import serializers

from product.models import Product
from product.serializers import ProductSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    sub_total = serializers.SerializerMethodField()
    quantity = serializers.ReadOnlyField()
    product = ProductSerializer(read_only=True)

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


class DeleteCartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Product
        ref_name = None
        fields = ('id',)


class UpdateCartItemSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        ref_name = None
        fields = ('id', 'quantity')

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity must be greater than or equal to 0.")
        return value

    def update(self, instance, validated_data):
        quantity = validated_data.get('quantity')

        if not quantity:
            instance.delete()
        else:
            instance.quantity = quantity
            instance.save()

        return instance
