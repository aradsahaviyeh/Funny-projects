from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse



from profile_app.models import Profile
from .forms import LoginForm, SignInForm
from .serializers import UserSerializer

class LoginView(View):
    template_name = "authentication_app/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('messages')
        return render(request, self.template_name, {'form': form})



class SignInView(View):
    template_name = "authentication_app/signin.html"

    def get(self, request):
        form = SignInForm(user=request.user)
        return render(request, self.template_name, {
            'form': form
        })



    def post(self, request):
        form = SignInForm(request.POST)

        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )

            user.set_password(form.cleaned_data['password1'])
            user.save()

            Profile.objects.create(
                user=user,
                profile_name = form.cleaned_data['username'],
                profile_username=form.cleaned_data['username'],
                email = form.cleaned_data['email'],
            )

            login(request, user)
            return redirect('messages')

        return render(request, self.template_name, {'form': form})

@api_view(['GET', 'POST'])
def api_user(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        return JsonResponse({'message': request.data})