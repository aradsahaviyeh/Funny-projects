from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("find_contact", views.find_contact , name="find_contact"),
    path("form_view/<str:_format>", views.form_view, name="form_view"),
    path("<str:name>", views.index, name="index"),
    path("send_message/<str:name>", views.send_message, name="send_message"),
]
