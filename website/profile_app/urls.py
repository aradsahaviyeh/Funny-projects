from django.urls import path
from .views import UserProfileView, ContactProfileView, api_profile

app_name = 'profile_app'
urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("contact/<int:profile_id>/", ContactProfileView.as_view(), name="contact_profile"),
    path("api/profile/", api_profile, name="api_profile"),
]
