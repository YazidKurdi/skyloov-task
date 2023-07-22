from django.urls import path
from .views import UserSignupView, UserActivateView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('activate/<str:uid>/<str:token>/', UserActivateView.as_view(), name='user_activate'),
]
