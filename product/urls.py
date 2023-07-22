from django.urls import path

from product import views

urlpatterns = [
    path('product-list-create/', views.ProductListCreate.as_view(), name='product-filter'),
]
