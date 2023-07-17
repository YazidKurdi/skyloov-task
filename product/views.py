from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer




class ProductList(APIView):

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


    def get(self, request):
        """
        API view to retrieve a single product
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListDetail(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Product.objects.all()
        filter_class = ProductFilter(request.query_params, queryset=queryset)

        serializer = ProductSerializer(filter_class.qs, many=True)
        return Response(serializer.data)
