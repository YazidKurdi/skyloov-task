from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters import rest_framework as filters

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer
from cart.utils import product_in_cart

from product.models import Product
from product.serializers import ProductSerializer

from drf_yasg.utils import swagger_auto_schema

class AddProductCart(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Add product to cart',
        operation_description='Given authenticated user and product_id in URL, product would be added to cart.',
        responses={
            201: 'Product added to cart successfully',
            400: 'Product already in cart',
            500: 'Internal server error',
        },
        tags=['Cart'],
    )
    def post(self, request, pk):

        try:
            # Get the product
            product = get_object_or_404(Product, id=pk)
            # Get the user's cart
            cart = Cart.objects.get(owner=request.user)
            # Validate and extract the quantity

            quantity = request.data.get('quantity', 1)
            if not isinstance(quantity, int):
                raise ValidationError('Quantity must be a number.')


            if not product_in_cart(cart, product):
                # Create the cart item
                CartItem.objects.create(cart=cart, product=product, quantity=quantity)
                return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_201_CREATED)

            return Response({'message': 'Product already in cart'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteProductCart(APIView):

    @swagger_auto_schema(
        operation_description='Given authenticated user and product_id in request body, product quantity in cart would be deleted.',
        operation_summary='Delete product from cart',
        responses={
            204: 'Product removed from cart successfully',
            404: 'Product not found',
        },
        tags=['Cart'],
    )
    def delete(self, request):

        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(owner=request.user)

        if product_in_cart(cart, product):
            cartitem = CartItem.objects.get(product_id=product_id, cart=cart)
            cartitem.delete()

            return Response({'message': 'Product removed from cart successfully'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

class UpdateProductCart(APIView):

    @swagger_auto_schema(
        operation_description='Given authenticated user and quantity in request body, product quantity in cart would be updated.',
        operation_summary='Update product quantity in cart',
        responses={
            200: 'Product quantity updated successfully',
            404: 'Product not found',
        },
        tags=['Cart'],
    )
    def put(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.get(owner=request.user)

        if product_in_cart(cart, product):
            cart_item = CartItem.objects.get(product_id=product_id, cart=cart)
            cart_item.quantity = quantity
            cart_item.save()

            return Response({'message': 'Product quantity updated successfully'},
                            status=status.HTTP_200_OK)

        return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class RetrieveCart(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Given authenticated user, Cart & CartItems informations would be retrieved.',
        operation_summary='Retrieve cart and cart items',
        responses={
            200: CartSerializer(many=True),
            404: 'Cart not found',
        },
        tags=['Cart'],
    )
    def get(self, request):
        cart = get_object_or_404(Cart,owner=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
