from django.db import models
from profile_app.models import Profile


# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="contacts")
    contact = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="contact_of")
    contact_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'contact')

    def __str__(self):
        return self.contact_name