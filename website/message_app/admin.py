from django.contrib import admin
from .models import Profile, Message, Contact, Chat

admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Contact)
admin.site.register(Chat)