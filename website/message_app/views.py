from django.shortcuts import render, redirect
from .models import Message

def message(request):
    if request.method == "POST":
        text = request.POST.get("message")
        Message.objects.create(
            text = text
        )
        return redirect("/messages/")
    
    messages = Message.objects.all()
    return render(request, "message_app/messages.html", {
        "messages":messages,
    })