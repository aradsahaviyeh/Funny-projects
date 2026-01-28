from django.db import models
from django.contrib.auth.models import User



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.text[:50]}"



class Contact(models.Model):
    user_name = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_contacts")
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contact_of")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} -> {self.contact}"