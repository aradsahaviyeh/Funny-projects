from django.urls import path
from . import views



urlpatterns = [
    path("", views.home, name="home"),
    path("messages/", views.message_view, name="messages"),
    path("messages/<int:profile_id>/", views.message_view, name="message_detail"),
    path("send_message/<str:profile_id>/", views.send_message, name="send_message"),
    path("find_message/", views.find_message, name="find_message"),
    path("profile/", views.user_profile, name="user_profile"),
    path("contact/<int:profile_id>/", views.contact_profile_view, name="contact_profile"),
    path("add_contact/",views.add_contact, name="add_contact"),
    path("my_contacts/", views.my_contacts, name="my_contacts"),
    path("login", views.login_view, name="login"),
]
