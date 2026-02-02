from django.urls import path
from . import views



urlpatterns = [
    path("", views.home, name="home"),
    path("messages/", views.message_view, name="messages"),
    path("messages/<int:profile_id>/", views.message_view, name="message_detail"),
    path("send_message/", views.send_message, name="send_message"),
    path("login", views.login_view, name="login"),
]
