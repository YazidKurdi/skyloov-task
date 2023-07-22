from django.urls import path

from cart import views

urlpatterns = [
    path('add-product/<int:pk>/', views.AddProductCart.as_view(), name='add-product'),
    path('delete-product/', views.DeleteCartItem.as_view(), name='delete-product'),
    path('update-product/', views.UpdateCartItem.as_view(), name='update-product'),
    path('all-products/', views.RetrieveCart.as_view(), name='all-products'),
]
