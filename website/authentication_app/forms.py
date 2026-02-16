from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from profile_app.models import Profile



class SignInForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'نام کاربری'
            }
        )
    )
    email = forms.EmailField(
        required=True,
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control bg-light border-0',
                'style': 'direction: rtl !important;',
                'placeholder': 'ایمیل'
            }
        )
    )
    password1 = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'رمز عبور'
            }
        )
    )

    password2 = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'تکرار رمز عبور'
            }
        )
    )


    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user



    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists() or Profile.objects.filter(profile_name=username).exists():
            raise ValidationError("این نام کاربری قبلا استفاده شده است.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists() or Profile.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل قبلا مورد استفاده قرار گرفته است.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("رمزهای عبور مطابقت ندارند")

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'نام کاربری'
            }
        )
    )

    email = forms.EmailField(
        required=True,
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control bg-light border-0',
                'style': 'direction: rtl !important;',
                'placeholder': 'ایمیل'
            }
        )
    )

    password = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control bg-light border-0',
                'placeholder': 'رمز عبور'
            }
        )
    )


    def clean(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        try:
            user = User.objects.get(username=username, email=email)
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                pass
        except User.DoesNotExist:
            raise ValidationError("نام کاربری و یا ایمیل نادرست است.")

        if not user.check_password(password):
            raise ValidationError("رمز عبور مطابقت ندارد.")


        return self.cleaned_data


