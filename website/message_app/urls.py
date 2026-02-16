from django.urls import path
from .views import *


urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("messages/", MessageView.as_view(), name="messages"),
    path("messages/<int:profile_id>/", MessageView.as_view(), name="message_detail"),
    path("send/<int:profile_id>/", SendMessageView.as_view(), name="send_message"),
    path("find/", FindMessageView.as_view(), name="find_message"),

]
