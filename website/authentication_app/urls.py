from django.urls import path
from rest_framework.decorators import api_view

from .views import LoginView, SignInView, api_user
from rest_framework.urlpatterns import format_suffix_patterns

app_name = "authentication_app"
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signin/', SignInView.as_view(), name='signin'),
    path("user_api/", api_user, name="user_api"),
]
