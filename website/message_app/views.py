from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .models import Message, Contact, Profile, Chat




    
def home(request):
    return render(request, "message_app/home.html")



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            Profile.objects.create(
                user=user,
                profile_name=username,
                email=email
            )

        login(request, user)
        return redirect("messages")

    return render(request, "message_app/login.html")




@login_required
def message_view(request, profile_id=None):
    my_profile = request.user.profile

    chats = Chat.objects.filter(
        profiles=my_profile
    ).prefetch_related(
        "profiles", "message_set"
    ).order_by("-last_chat")

    chat_items = []
    selected_chat_messages = []
    contact_profile = None
    contact_name = None
    message_detail = False

    for chat in chats:
        other_profile = chat.profiles.exclude(id=my_profile.id).first()
        if not other_profile:
            continue

        contact = Contact.objects.filter(
            user=my_profile,
            contact=other_profile
        ).first()

        display_name = (
            contact.contact_name if contact else other_profile.profile_name
        )

        last_message = chat.message_set.order_by("-created_at").first()

        chat_items.append({
            "chat": chat,
            "profile": other_profile,
            "display_name": display_name,
            "last_message": last_message,
        })


    if profile_id:
        is_detail = True
        message_detail = True
        contact_profile = get_object_or_404(Profile, id=profile_id)

        contact = Contact.objects.filter(
            user=my_profile,
            contact=contact_profile
        ).first()

        contact_name = (
            contact.contact_name if contact else contact_profile.profile_name
        )

        selected_chat = Chat.objects.filter(
            profiles=my_profile
        ).filter(
            profiles=contact_profile
        ).first()

        if selected_chat:
            selected_chat_messages = selected_chat.message_set.order_by("created_at")

    return render(request, "message_app/messages.html", {
        "message_detail": message_detail,
        "chat_items": chat_items,
        "messages": selected_chat_messages,
        "contact": contact_profile,
        "contact_name": contact_name,
    })


@login_required(login_url="login")
def my_contacts(request):
    contacts = Contact.objects.filter(
        user = request.user.profile
    )
    return render(
        request,
        "message_app/my_contacts.html",
        {
            "contacts" : contacts,
        }
    )


@login_required
def send_message(request, profile_id):
    if request.method != "POST":
        return HttpResponseBadRequest()

    sender_profile = request.user.profile
    receiver_profile = get_object_or_404(Profile, id=profile_id)

    if sender_profile == receiver_profile:
        return HttpResponseBadRequest("نمی‌تونی به خودت پیام بدی")

    text = request.POST.get("text")
    if not text:
        return HttpResponseBadRequest("پیام خالیه")

    chat = Chat.objects.filter(
        profiles=sender_profile
    ).filter(
        profiles=receiver_profile
    ).first()

    if not chat:
        chat = Chat.objects.create()
        chat.profiles.add(sender_profile, receiver_profile)

    Message.objects.create(
        sender=sender_profile,
        chat=chat,
        text=text
    )

    return redirect("message_detail", profile_id)




@login_required
def add_contact(request):
    if request.method == "POST":
        profile = request.user.profile
        email = request.POST.get("email")
        contact_name = request.POST.get("contact_name")

        try:
            contact_profile = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            return HttpResponseBadRequest("کاربر پیدا نشد")

        if contact_profile == profile:
            return HttpResponseBadRequest("نمی‌تونی خودتو اضافه کنی")

        if Contact.objects.filter(user=profile, contact=contact_profile).exists():
            return HttpResponseBadRequest("این کانتکت قبلاً اضافه شده")

        Contact.objects.create(
            user=profile,
            contact=contact_profile,
            contact_name=contact_name
        )

        return redirect("messages")

    return render(request, "message_app/add_contact.html")





@login_required
def find_message(request):
    content = request.GET.get("search", "")
    profiles = None
    if "@" in content:
        profiles = Profile.objects.filter(
            profile_username__icontains=content
        )

    contacts = Contact.objects.filter(
        contact_name__icontains=content
    )

    return render(
        request,
        "message_app/find_message.html",
        {
            "profiles": profiles,
            "contacts": contacts,
        }
    )


@login_required
def user_profile(request):
    profile = request.user.profile
    return render(
        request,
        "message_app/profile.html",
        {"profile": profile}
    )

@login_required
def contact_profile_view(request, profile_id):
    contact = get_object_or_404(Profile, id=profile_id)
    return render(
        request,
        "message_app/contact_profile.html",
        {"contact": contact}
    )
