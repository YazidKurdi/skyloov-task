from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters import rest_framework as filters

from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer




# class ProductList(APIView):
#
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]
#
#
#     def get(self, request):
#         """
#         API view to retrieve a single product
#         """
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class ProductListDetail(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     filter_backends = [OrderingFilter]  # Add the OrderingFilter backend
#
#     def get(self, request):
#         queryset = Product.objects.all()
#         filter_class = ProductFilter(request.query_params, queryset=queryset)
#
#         # Apply the filtering and ordering
#         filtered_queryset = filter_class.qs
#         ordered_queryset = self.filter_queryset(filtered_queryset)
#
#         serializer = ProductSerializer(ordered_queryset, many=True)
#         return Response(serializer.data)

class ProductListDetail(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,SearchFilter,OrderingFilter)

    filterset_class = ProductFilter
    ordering_fields = ['rating']
    search_fields = ['description']
