from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import UpdateView
from django.urls import reverse

from .forms import RegisterForm, ProfileForm, LoginForm


class AthenticationView(View):
    """Registration and login page."""
    template_name = "account/authentication.html"

    def get(self, request):
        """Connects two forms with prefixes: reg, login."""
        context = {
            "register_form": RegisterForm(prefix="reg"),
            "login_form": LoginForm(prefix="login"),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        """Creates an account and logs in or simply logs into an existing account."""
        if "register_submit" in request.POST:
            register_form = RegisterForm(request.POST, prefix="reg")
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect("content:home")
            login_form = LoginForm(prefix="login")
            messages.error(request, register_form.errors)
            
        elif "login_submit" in request.POST:
            login_form = LoginForm(request, data=request.POST, prefix="login")
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("content:home")
            register_form = RegisterForm(prefix="reg")
       
        else:
            register_form = RegisterForm(prefix="reg")
            login_form = LoginForm(prefix="login")

        return render(request, self.template_name, {
            "register_form": register_form,
            "login_form": login_form,
        })


def log_out(request):
    """Logs out of account."""
    if request.user.is_authenticated:
        logout(request)
    return redirect("content:home")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Passes the form ProfileForm to the template."""
    model = get_user_model()
    form_class = ProfileForm
    template_name = "account/profile.html"

    def get_success_url(self):
        return reverse("account:profile", args=[self.get_object().pk])
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Breadcrumb navigation."""
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [{"name": "Home", "url": reverse("content:home")},
                                  {"name": "User profile", "url": ""}]
        return context 