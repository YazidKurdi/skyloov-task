from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class TokenObtainPairView(TokenObtainPairView):

    @swagger_auto_schema(
        operation_summary="Retrieve access and refresh tokens",
        operation_description="This endpoint retrieves access and refresh tokens when a user logs in.",
        tags=["Login"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshView(TokenRefreshView):

    @swagger_auto_schema(
        operation_summary="Retrieve access token",
        operation_description="This endpoint retrieves an access token when a refresh token is supplied.",
        tags=["Login"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)