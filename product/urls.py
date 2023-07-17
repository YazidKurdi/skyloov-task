from django.urls import path

from product import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('product-detail/', views.ProductListDetail.as_view(), name='product-filter'),
]
