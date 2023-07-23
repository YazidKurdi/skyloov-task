from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .token import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Skyloov Backend API",
        default_version='v1',
        description="The documentation below contains three main endpoints (Cart, Product and Login),"
                    " Cart endpoint's and Product (POST request) require user authentication while Product(GET request) does not. \n\n"
                    "Login in through the 'Django Login' button and insert username and password,"
                    " an access token will be generated that can be used to access the endpoints that need authentication. \n\n",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/product/', include('product.urls')),
    path('api/cart/', include('cart.urls')),
    path('', include('account.urls')),
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
