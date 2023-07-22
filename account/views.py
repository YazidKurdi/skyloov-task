from coreapi.compat import force_text
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer
from .tasks import send_welcome_email_task


class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="Create a new user",
        operation_description="This endpoint generates a new user, given a username,email and password.",
        responses={200: UserSerializer(many=True),
                   400: 'Bad request',
                   500: 'Internal server error'},
        tags=["Signup"]
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new user
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Mark the user as inactive upon creation
            user = serializer.save(is_active=False)
            # Send the welcome email with the activation link
            send_welcome_email_task.apply_async(args=[user.id], countdown=10)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivateView(APIView):
    def get(self, request, uid, token):
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({'message': 'Account activated'},status=status.HTTP_200_OK)
            else:
                # You can add an error message here if needed
                return Response({'error': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # You can add an error message here if needed
            return Response({'error': 'Invalid activation link'}, status=status.HTTP_400_BAD_REQUEST)