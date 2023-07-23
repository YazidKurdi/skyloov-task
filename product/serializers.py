from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category',
            'brand',
            'min_price',
            'max_price',
            'rating',
            'description',
            'min_quantity',
            'max_quantity',
            'created_at')

    def get_created_at(self, instance):
        """
        Get the formatted string representation of the product's creation date.
        """

        return instance.created_at.strftime("%d-%m-%Y %H:%M:%S")

    def validate(self, data):
        """
        Validate the data for the Product serializer (min_price <= max_price) and (min_quantity <= max_quantity).
        """

        if 'min_price' in data and 'max_price' in data:
            min_price = data['min_price']
            max_price = data['max_price']
            if min_price > max_price:
                raise ValidationError("min_price must be less than or equal to max_price.")

        if 'min_quantity' in data and 'max_quantity' in data:
            min_quantity = data['min_quantity']
            max_quantity = data['max_quantity']
            if min_quantity > max_quantity:
                raise ValidationError("min_quantity must be less than or equal to max_quantity.")

        return data
