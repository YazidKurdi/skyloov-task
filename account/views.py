from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from .serializers import UserSerializer


@swagger_auto_schema(
    operation_summary="Create a new user",
    operation_description="This endpoint generates a new user, given a username,email and password.",
    responses={200: UserSerializer(many=True),
               400: 'Bad request',
               500: 'Internal server error'},
    tags=["Sign-up"],
)
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer