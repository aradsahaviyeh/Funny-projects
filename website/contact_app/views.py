from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ContactForm
from .models import Contact
from profile_app.models import Profile


class MyContactsView(LoginRequiredMixin, ListView):
    model = Contact
    login_url = "authentication_app:login"
    template_name = "contact_app/my_contacts.html"
    context_object_name = "contacts"

    def get_queryset(self):
        return Contact.objects.filter(
            user=self.request.user.profile
        )



class AddContactView(LoginRequiredMixin, View):
    login_url = "authentication_app:login"
    template_name = "contact_app/add_contact.html"


    def get(self, request):
        form = ContactForm(user=request.user.profile)
        return render(request, self.template_name, {
            "form": form
        })

    def post(self, request):
        form = ContactForm(request.POST, user=request.user.profile)
        if form.is_valid():
            email = form.cleaned_data['email']
            contact_name = form.cleaned_data['contact_name']
            Contact.objects.create(
                user=request.user.profile,
                contact=Profile.objects.get(email=email),
                contact_name=contact_name
            )
            return redirect("contact_app:my_contacts")
        return render(request, self.template_name, {
            "form": form
        })
