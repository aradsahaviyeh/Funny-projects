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



class Chat(models.Model):
    profiles = models.ManyToManyField(Profile)
    created_at = models.DateTimeField(auto_now_add=True)
    last_chat = models.DateTimeField(auto_now=True)

    def __str__(self):
        profiles = [p.profile_name for p in self.profiles.all()]
        return f"{profiles} are talking together"





class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text[:20]} in chat : {self.chat}"


class Contact(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="contacts")
    contact = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="contact_of")
    contact_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'contact') 

    def __str__(self):
        return self.contact_name