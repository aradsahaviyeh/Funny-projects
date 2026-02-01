from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Message, Contact, Profile
from django.db import models



def home(request):
    return render(request, "message_app/home.html")


def messages(request, contact_name=None):
    profile = Profile.objects.get(user=request.user)
    contacts = Contact.objects.filter(user=profile) | Contact.objects.filter(contact=profile)
    if contact_name:
        contact = Contact.objects.get(user=profile, contact_name=contact_name)
        messages = Message.objects.filter(sender=profile, receiver=contact.contact)\
        | Message.objects.filter(sender=contact.contact, receiver=profile)
        return render(
            request,
            "message_app/messages.html",
            {
                "profile" : profile,
                "contacts":contacts,
                "contact":contact,
                "messages": messages
            }
            )
    else:
        return render(
            request,
            "message_app/messages.html",
            {
                "contacts":contacts,
            }
            ) 

def send_message(request):
    if request.method == "POST":
        text = request.POST.get("text")
        name = request.POST.get("name")

        if text and name:
            user_profile = Profile.objects.get(user=request.user)
            contact = Contact.objects.get(
                user=user_profile,
                contact_name=name
            )

            Message.objects.create(
                sender=user_profile,
                receiver=contact.contact,
                text=text
            )

            return redirect("messages", name)

    return redirect("messages")