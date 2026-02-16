from os import name

from django import forms
from django.core.exceptions import ValidationError
from django.template.context_processors import request

from .models import Contact
from profile_app.models import Profile

class ContactForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-light border-0',
            'placeholder': 'example@email.com',
        })
    )
    contact_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light border-0',
            'placeholder': 'مثال: علی رضایی',
        })
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            contact_profile = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            raise ValidationError("ایمیل در بانک موجود نمیباشد.")
        if Contact.objects.filter(user=self.user, contact=contact_profile).exists():
            raise ValidationError("این کاربر قبلا اضافه شده است.")

        return email
