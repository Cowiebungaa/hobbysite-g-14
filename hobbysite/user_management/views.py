from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Profile

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = Profile.objects.get_or_create(user=request.user)[0]
        context = {'profile': profile}
        return render(request, 'user_management/profile.html', context)