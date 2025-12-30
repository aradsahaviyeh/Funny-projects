from django.db import models
# Create your models here.


class Message(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text