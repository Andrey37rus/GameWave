from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login, logout
from django.views import View
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileUpdateForm

from .models import Profile


class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        login(self.request, self.object)
        return response


class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("myauth:login")


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'myauth/profile_update.html'
    success_url = reverse_lazy('myauth:about-me')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        user = form.save()
        profile_form = ProfileUpdateForm(self.request.POST, self.request.FILES, instance=user.profile)
        if profile_form.is_valid():
            profile_form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile)
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = 'myauth/user_confirm_delete.html'
    success_url = reverse_lazy("myauth:login")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
