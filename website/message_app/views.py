from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Message, Contact
from django.db import models







def index(request, name=None):
    contacts = Contact.objects.filter(user=request.user)
    try:
        contact = Contact.objects.get(user_name=name, user=request.user).contact
        messages = Message.objects.filter(
            models.Q(sender=request.user, receiver=contact) |
            models.Q(sender=contact, receiver=request.user)
        ).order_by("created_at")
        
        return render(
            request,
            "message_app/messages.html",
            {
                "contacts": contacts,
                "messages": messages,  # فقط یک لیست پیام داریم
                "user_name": name,
                "contact": contact,  # اضافه کردن contact برای استفاده در تمپلیت
            }
        )
    except:
        return render(
            request,
            "message_app/messages.html",
            {
                "user_name" : name,
                "contacts": contacts,
            }
        )


def find_contact(request):
    name = request.GET.get("name")
    user = request.user
    contacts = Contact.objects.filter(user_name__contains=name, user=user)
    return render(
        request,
        "message_app/find_contact.html",
        {
            "contacts" : contacts,
        }
    )



def send_message(request, name=None):
    if request.method == "POST" and name:
        sender = request.user
        contact = Contact.objects.get(user_name=name, user=sender)
        receiver = contact.contact
        text = request.POST.get("message")
        message = Message(sender=sender, receiver=receiver, text=text)
        try:
            message.save()
            return HttpResponseRedirect(reverse("index", args=[name]))
        except:
            return HttpResponseBadRequest("your message hasn't save.")
    return redirect("index")




def form_view(request, _format):
    if request.method == "POST" and _format == "contact":
        user_name = request.POST.get("name")
        email = request.POST.get("email")
        contact_user = User.objects.get(email=email)
        if contact_user:
            contact = Contact(user_name=user_name, user=request.user, contact=contact_user)
            contact.save()
            return redirect("index")
    return render(
        request,
        "message_app/form.html",
    )