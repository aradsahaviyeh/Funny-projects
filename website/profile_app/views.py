from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProfileSerializer

from .models import Profile

class UserProfileView(LoginRequiredMixin, TemplateView):
    login_url = "authentication_app:login"
    template_name = "profile_app/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.request.user.profile
        return context

class ContactProfileView(LoginRequiredMixin, DetailView):
    login_url = "authentication_app:login"
    model = Profile
    template_name = "profile_app/profile.html"
    context_object_name = "contact"
    pk_url_kwarg = "profile_id"


@api_view(["GET"])
def api_profile(request):
    porfiles = Profile.objects.all()
    serializer = ProfileSerializer(porfiles, many=True)
    return Response(serializer.data)