from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.views.generic import UpdateView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import RegisterForm


class AthenticationView(View):
    template_name = "account/authentication.html"

    def get(self, request):
        context = {
            "register_form": RegisterForm(prefix="reg"),
            "login_form": AuthenticationForm(prefix="login"),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        if "register_submit" in request.POST:
            register_form = RegisterForm(request.POST)
            login_form = AuthenticationForm(prefix="login")
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect("content:home")
            messages.error(request, register_form.errors)
            
        elif "login_submit" in request.POST:
            login_form = AuthenticationForm(request, data=request.POST, prefix="login")
            register_form = RegisterForm(prefix="reg")
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect("content:home")
       
        else:
            register_form = RegisterForm(prefix="reg")
            login_form = AuthenticationForm(prefix="login")

        return render(request, self.template_name, {
            "register_form": register_form,
            "login_form": login_form,
        })
    

def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("content:home")


class ProfileUpdateView(UpdateView):
    model = get_user_model()
    template_name = "account/profile.html"
    fields = ["username", "first_name", "last_name", "country", "age", "password", "avatar"]

    def get_success_url(self):
        return reverse_lazy("account:profile", args=[self.request.user.pk])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["breadcrumbs"] = [{"name": "Home", "url": reverse_lazy("content:home")}, {"name": "User profile", "url": ""}]
        return context 