from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, UpdateView, DetailView
from django.urls import reverse_lazy

from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm
from .models import Profile


class UserRegistration(FormView):
    form_class = UserRegistrationForm
    template_name = 'accounts/registration.html'
    success_url = reverse_lazy('movies:view-movies')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, "Account successfuly created")
        return super(UserRegistration, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error during creating an account")
        return super(UserRegistration, self).form_invalid(form)


class UserAuthentication(FormView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('movies:view-movies')

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, "You successfully logged")
        return super(UserAuthentication, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error during login")
        return super(UserAuthentication, self).form_invalid(form)


def logout_view(request):
    logout(request)
    messages.success(request, "You successfuly logged out")
    return redirect('movies:view-movies')


class ViewProfile(DetailView):
    model = Profile
    template_name = 'accounts/profile/view_profile.html'
    context_object_name = 'custom_user'
    slug_field = 'username'
    slug_url_kwarg = 'username_slug'


class EditProfile(UpdateView):
    model = Profile
    form_class = UserProfileUpdateForm
    template_name = 'accounts/profile/edit_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username_slug'

    def get_success_url(self):
        print(self.kwargs)
        username_slug = self.kwargs['username_slug']
        return reverse_lazy('accounts:edit-profile', kwargs={'username_slug': username_slug})
