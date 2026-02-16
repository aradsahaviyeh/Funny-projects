from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView


# models : ---->
from .models import Message, Chat
from profile_app.models import Profile
from contact_app.models import Contact






class HomeView(TemplateView):
    template_name = "message_app/home.html"


class MessageView(LoginRequiredMixin, View):
    login_url = "authentication_app:login"
    template_name = "message_app/messages.html"

    def get(self, request, profile_id=None):
        my_profile = request.user.profile

        chats = Chat.objects.filter(
            profiles=my_profile
        ).prefetch_related("profiles", "message_set").order_by("-last_chat")

        chat_items = []

        for chat in chats:
            other_profile = chat.profiles.exclude(id=my_profile.id).first()
            if not other_profile:
                continue

            contact = Contact.objects.filter(
                user=my_profile,
                contact=other_profile
            ).first()

            display_name = (
                contact.contact_name
                if contact else
                other_profile.profile_name
            )

            last_message = chat.message_set.order_by("-created_at").first()

            chat_items.append({
                "chat": chat,
                "profile": other_profile,
                "display_name": display_name,
                "last_message": last_message,
            })


        selected_messages = []
        contact_profile = None
        contact_name = None
        message_detail = False

        if profile_id:
            message_detail = True
            contact_profile = get_object_or_404(Profile, id=profile_id)

            contact = Contact.objects.filter(
                user=my_profile,
                contact=contact_profile
            ).first()

            contact_name = (
                contact.contact_name
                if contact else
                contact_profile.profile_name
            )

            selected_chat = Chat.objects.filter(
                profiles=my_profile
            ).filter(
                profiles=contact_profile
            ).first()

            if selected_chat:
                selected_messages = selected_chat.message_set.order_by("created_at")

        context = {
            "chat_items": chat_items,
            "messages": selected_messages,
            "contact": contact_profile,
            "contact_name": contact_name,
            "message_detail": message_detail,
        }

        return render(request, self.template_name, context)





class SendMessageView(LoginRequiredMixin, View):
    login_url = "authentication_app:login"
    def post(self, request, profile_id):
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

        return redirect("message_detail", profile_id=profile_id)




class FindMessageView(LoginRequiredMixin, View):
    login_url = "authentication_app:login"
    template_name = "message_app/find_message.html"

    def get(self, request):
        content = request.GET.get("search", "")
        profiles = None

        if "@" in content:
            profiles = Profile.objects.filter(
                profile_username__icontains=content
            )

        contacts = Contact.objects.filter(
            contact_name__icontains=content
        )

        return render(request, self.template_name, {
            "profiles": profiles,
            "contacts": contacts,
        })


