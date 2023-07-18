from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters import rest_framework as filters

from cart.models import Cart
from cart.serializers import CartSerializer
from product.models import Product


class AddRemoveProductCart(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """
        API view to add a single product to cart
        """
        product = get_object_or_404(Product, id=pk)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)

        return Response("Product added to cart successfully", status=status.HTTP_201_CREATED)

    def put(self,request,pk):
        """

        """

        cart = Cart.objects.get(user=request.user)
        if not cart.products.filter(id=pk).exists():
            return Response("Product not found", status=status.HTTP_404_NOT_FOUND)

        product = get_object_or_404(Product, id=pk)





        serializer = CartSerializer(cart,data=request.data)

        # Check if the serializer is valid
        if serializer.is_valid():

            serializer.save()
            # Return the serialized data
            return Response(serializer.data)
        # Return the serializer errors with a bad request status code
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, pk):
        """
        API view to remove a single product from cart
        """
        product = get_object_or_404(Product, id=pk)
        cart = Cart.objects.get(user=request.user)

        if product in cart.products.all():
            cart.products.remove(product)
            return Response("Product removed from cart successfully", status=status.HTTP_204_NO_CONTENT)

        return Response("Product not found", status=status.HTTP_404_NOT_FOUND)


