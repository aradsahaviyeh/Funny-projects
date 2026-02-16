from django.urls import path

from .views import *


app_name = 'contact_app'
urlpatterns = [
    path("contacts/", MyContactsView.as_view(), name="my_contacts"),
    path("add-contact/", AddContactView.as_view(), name="add_contact"),
]