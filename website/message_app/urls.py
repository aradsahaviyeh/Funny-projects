from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("messages", views.messages, name="messages"),
    path("messages/<str:contact_name>", views.messages, name="messages"),
    path("send_message/", views.send_message, name="send_message"),
]
