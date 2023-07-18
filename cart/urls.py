from django.urls import path

from cart import views

urlpatterns = [
    # path('products/', views.ProductList.as_view()),
    path('add-product/<int:pk>/', views.AddRemoveProductCart.as_view(), name='add-product'),
]
