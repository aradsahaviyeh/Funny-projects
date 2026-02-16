from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, default='')
    profile_username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    profile_name = models.CharField(max_length=150)
    profile_bio = models.TextField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to="images/", null=True, blank=True)
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile_name

