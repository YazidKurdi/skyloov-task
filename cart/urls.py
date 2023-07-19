from django.urls import path

from cart import views

urlpatterns = [
    # path('products/', views.ProductList.as_view()),
    # path('add-product/<int:pk>/', views.AddRemoveProductCart.as_view(), name='add-product'),
    path('add-product/<int:pk>/', views.AddProductCart.as_view(), name='add-product'),
    path('delete-product/', views.DeleteProductCart.as_view(), name='delete-product'),
    path('update-product/', views.UpdateProductCart.as_view(), name='update-product'),
    path('all-products/', views.RetrieveCart.as_view(), name='all-products'),
]

