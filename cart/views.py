from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404

from cart.models import Cart, CartItem
from cart.serializers import (
    CartSerializer,
    DeleteCartItemSerializer,
    UpdateCartItemSerializer,
)
from cart.utils import product_in_cart
from product.models import Product


class AddProductCart(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Add product to cart',
        operation_description='Given authenticated user and product_id in URL, Product would be added to Cart as a CartItem.',
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
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteCartItem(APIView):

    @swagger_auto_schema(
        operation_description='Given authenticated user and product_id in request body,CartItem in Cart would be deleted.',
        operation_summary='Delete CartItem from Cart',
        responses={
            204: 'Product removed from cart successfully',
            400: "{'product_id': [ErrorDetail(string='A valid integer is required.', code='invalid')]}",
            404: 'Product not in cart',
        },
        request_body=DeleteCartItemSerializer,
        tags=['Cart'],
    )
    def delete(self, request):

        serializer = DeleteCartItemSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'error': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

        product_id = serializer.validated_data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart = get_object_or_404(Cart, owner=request.user)

        if product_in_cart(cart, product):
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.delete()

            return Response({'message': 'Product removed from cart successfully'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'message': 'Product already not in cart'}, status=status.HTTP_404_NOT_FOUND)


class UpdateCartItem(APIView):

    @swagger_auto_schema(
        operation_description='Given authenticated user, CartItem ID & Quantity in request body, CartItem quantity in Cart would be updated.',
        operation_summary='Update CartItem quantity in Cart',
        responses={
            200: 'CartItem quantity updated successfully',
            404: 'CartItem not found',
        },
        request_body=UpdateCartItemSerializer,
        tags=['Cart'],
    )
    def put(self, request):
        serializer = UpdateCartItemSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'error': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

        cart_item_id = serializer.data.get('id')
        product = get_object_or_404(Product, id=cart_item_id)
        cart = get_object_or_404(Cart, owner=request.user)

        if product_in_cart(cart, product):
            cart_item = get_object_or_404(CartItem, product=product, cart=cart)
            serializer.update(cart_item, serializer.validated_data)

            return Response({'message': 'CartItem quantity updated successfully'},
                            status=status.HTTP_200_OK)

        return Response({'message': 'CartItem not found in Cart'}, status=status.HTTP_404_NOT_FOUND)


class RetrieveCart(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Given authenticated user, Cart & CartItems information would be retrieved.',
        operation_summary='Retrieve Cart and CartItem(s)',
        responses={
            200: CartSerializer(many=True),
            404: 'Cart not found',
        },
        tags=['Cart'],
    )
    def get(self, request):
        cart = get_object_or_404(Cart, owner=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
