from django.db import models
from django.contrib.auth.models import User
from profile_app.models import Profile


class Chat(models.Model):
    profiles = models.ManyToManyField(Profile)
    created_at = models.DateTimeField(auto_now_add=True)
    last_chat = models.DateTimeField(auto_now=True)

    def __str__(self):
        profiles = [p.profile_name for p in self.profiles.all()]
        return f"{profiles} are talking together"



class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, default="")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} sent : {self.text[:20]} in chat : {self.chat}"


