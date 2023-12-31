from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import SearchPagination
from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer


class ProductListCreate(generics.ListCreateAPIView):
    """
    API view for listing and creating products.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = []

    # Queryset and serializer
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Filtering, ordering and search
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['rating']
    search_fields = ['description']

    # Pagination
    pagination_class = SearchPagination

    def get_permissions(self):
        """
        Return the list of permissions that should be applied to the view.
        Only applies IsAuthenticated permission for POST requests.
        """
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        else:
            return []

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
        Get a list of products.
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
        Create a new product.
        """
        return super().post(request, *args, **kwargs)
