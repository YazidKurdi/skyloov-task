from rest_framework import serializers

from .models import Product


from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class ProductSerializer(serializers.ModelSerializer):

    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    min_quantity = serializers.IntegerField()
    max_quantity = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ('name',
                  'category',
                  'brand',
                  'min_price',
                  'max_price',
                  'rating',
                  'description',
                  'min_quantity',
                  'max_quantity',
                  'created_at')

    def validate(self, data):
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
