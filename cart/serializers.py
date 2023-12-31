from rest_framework import serializers

from product.models import Product
from product.serializers import ProductSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):

    sub_total = serializers.SerializerMethodField()
    quantity = serializers.ReadOnlyField()
    product = ProductSerializer(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'quantity', 'sub_total', 'created_at', 'updated_at')

    def get_sub_total(self, obj):
        """
        Calculate and return the subtotal for the CartItem.
        """
        return obj.subTotal

    def get_created_at(self, instance):
        """
        Return the formatted created_at timestamp.
        """
        return instance.created_at.strftime("%d-%m-%Y %H:%M:%S")

    def get_updated_at(self, instance):
        """
        Return the formatted updated_at timestamp.
        """
        return instance.updated_at.strftime("%d-%m-%Y %H:%M:%S")


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    num_of_items = serializers.SerializerMethodField()
    cart_total = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'owner', 'created_at', 'num_of_items', 'cart_total', 'cart_items')

    def get_num_of_items(self, obj):
        """
        Return the number of items in the Cart.
        """
        return obj.num_of_items

    def get_cart_total(self, obj):
        """
        Return the total price of the Cart.
        """
        return obj.cart_total

    def get_created_at(self, instance):
        """
        Return the formatted created_at timestamp.
        """
        return instance.created_at.strftime("%d-%m-%Y %H:%M:%S")


class DeleteCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = Product
        ref_name = None
        fields = ('product_id',)


class UpdateCartItemSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = CartItem
        ref_name = None
        fields = ('product_id', 'quantity')

    def validate_quantity(self, value):
        """
        Validate that the quantity is greater than or equal to 0.
        """
        if value < 0:
            raise serializers.ValidationError("Quantity must be greater than or equal to 0.")
        return value

    def update(self, instance, validated_data):
        """
        Update the quantity of the CartItem or delete it if quantity is zero.
        """
        quantity = validated_data.get('quantity')

        if not quantity:
            instance.delete()
        else:
            instance.quantity = quantity
            instance.save()

        return instance
