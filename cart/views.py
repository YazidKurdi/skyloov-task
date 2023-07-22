from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
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


class BaseCartAction(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_product_cart(self, request):
        cart = get_object_or_404(Cart, owner=request.user)
        return cart

    def get_product_from_cart(self, request):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        return product

    def get_cart_item(self, cart, product):
        return get_object_or_404(CartItem, product=product, cart=cart)

class AddProductCart(BaseCartAction):

    @swagger_auto_schema(
        operation_summary='Add CartItem to Cart',
        operation_description='Given an authenticated user and a product_id in URL, Product would be added to Cart as a CartItem.',
        responses={
            201: 'Product added to cart successfully',
            400: 'Product already in cart | Serialization error',
            404: 'Detail not found (Product, Cart or CartItem not found)',
        },
        request_body=UpdateCartItemSerializer,
        tags=['Cart'],
    )
    def post(self, request):
        serializer = UpdateCartItemSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        product = self.get_product_from_cart(request)
        cart = self.get_product_cart(request)

        if product_in_cart(cart, product):
            return Response({'message': 'Product already in cart'}, status=status.HTTP_400_BAD_REQUEST)

        quantity = serializer.validated_data.get('quantity', 1)
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        return Response({'message': 'Product added to cart successfully'}, status=status.HTTP_201_CREATED)


class DeleteCartItem(BaseCartAction):

    @swagger_auto_schema(
        operation_description='Given and authenticated user and a product_id in request body,CartItem in Cart would be deleted.',
        operation_summary='Delete CartItem from Cart',
        responses={
            204: 'Product removed from cart successfully',
            400: 'Product already in cart | Serialization error',
            404: 'Detail not found (Product, Cart or CartItem not found)',
        },
        request_body=DeleteCartItemSerializer,
        tags=['Cart'],
    )
    def delete(self, request):
        serializer = DeleteCartItemSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'error': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

        product = self.get_product_from_cart(request)
        cart = self.get_product_cart(request)

        if product_in_cart(cart, product):
            cart_item = self.get_cart_item(cart, product)
            cart_item.delete()
            return Response({'message': 'Product removed from cart successfully'}, status=status.HTTP_204_NO_CONTENT)

        return Response({'message': 'Product not in cart'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateCartItem(BaseCartAction):

    @swagger_auto_schema(
        operation_description='Given an authenticated user, CartItem ID & Quantity in request body, CartItem quantity in Cart would be updated.',
        operation_summary='Update CartItem quantity in Cart',
        responses={
            200: 'CartItem quantity updated successfully',
            400: 'CartItem not found in Cart',
            404: 'Detail not found (Product, Cart or CartItem not found)',
        },
        request_body=UpdateCartItemSerializer,
        tags=['Cart'],
    )
    def put(self, request):
        serializer = UpdateCartItemSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'error': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)

        product = self.get_product_from_cart(request)
        cart = self.get_product_cart(request)

        if product_in_cart(cart, product):
            cart_item = self.get_cart_item(cart, product)
            serializer.update(cart_item, serializer.validated_data)
            return Response({'message': 'CartItem quantity updated successfully'}, status=status.HTTP_200_OK)

        return Response({'message': 'CartItem not found in Cart'}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveCart(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description='Given an authenticated user, Cart & CartItems information would be retrieved.',
        operation_summary='Retrieve Cart and CartItem(s)',
        responses={
            200: CartSerializer(many=True),
            404: 'Detail not found (Cart not found)',
        },
        tags=['Cart'],
    )
    def get(self, request):
        cart = get_object_or_404(Cart, owner=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data,status=status.HTTP_200_OK)
