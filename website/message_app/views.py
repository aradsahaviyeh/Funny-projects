from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Message, Contact, Profile, Chat
from django.db import models



def home(request):
    return render(request, "message_app/home.html")



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        user, created = User.objects.get_or_create(username=username, email=email)
        if created:
            Profile.objects.create(user=user, profile_name=username)
        login(request, user)
        return redirect("messages")
    return render(
        request,
        "message_app/login.html"
    )


def message_view(request, profile_id=None):
    if not request.user.is_authenticated:
        return redirect("login")

    my_profile = Profile.objects.get(user=request.user)

    chats = Chat.objects.filter(profiles=my_profile).prefetch_related("profiles", "message_set").order_by("-last_chat")

    chat_items = []
    selected_chat_messages = []
    contact_profile = None

    for chat in chats:
        other_profile = chat.profiles.exclude(id=my_profile.id).first()
        if not other_profile:
            continue

        contact = Contact.objects.filter(user=my_profile, contact=other_profile).first()
        display_name = contact.contact_name if contact else other_profile.profile_name
        last_message = chat.message_set.order_by("-created_at").first()

        chat_items.append({
            "chat": chat,
            "profile": other_profile,
            "display_name": display_name,
            "last_message": last_message,
        })

    # Selected chat
    if profile_id:
        try:
            contact_profile = Profile.objects.get(id=profile_id)
            try:
                contact_name = Contact.objects.get(user=my_profile, contact=contact_profile).contact_name
            except:
                contact_name = contact_profile.profile_name
            selected_chat = Chat.objects.filter(profiles=my_profile).filter(profiles=contact_profile).first()
            if selected_chat:
                selected_chat_messages = selected_chat.message_set.order_by("created_at")
        except Profile.DoesNotExist:
            contact_profile = None
            selected_chat_messages = []

    return render(request, "message_app/messages.html", {
        "chat_items": chat_items,
        "messages": selected_chat_messages,
        "contact": contact_profile,
        "contact_name": contact_name,
    })






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