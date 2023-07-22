from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters import rest_framework as filters

from . import SearchPagination
from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer


class ProductList(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['rating']
    search_fields = ['description']
    pagination_class = SearchPagination

    @swagger_auto_schema(
        operation_summary="Retrieve a list of products",
        operation_description="This endpoint retrieves a list of products with optional filtering, ordering, and search capabilities.",
        responses={200: ProductSerializer(many=True),
                   400: 'Bad request',
                   500: 'Internal server error'},
        tags=["Product"],
    )
    def get(self, request, *args, **kwargs):
        """
        Get a list of products
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new product",
        operation_description="This endpoint creates a new product.",
        request_body=ProductSerializer,
        responses={201: ProductSerializer(),
                   400: 'Bad request',
                   500: 'Internal server error'},
        tags=["Product"],
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new product
        """
        return super().post(request, *args, **kwargs)
