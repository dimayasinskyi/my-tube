from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages

from ..mixins import MongoMixin
from .models import User
from .forms import RegisterForm


class ListAdmin(MongoMixin, ListView):
    """List of users in the admin panel."""
    model = User
    template_name = "admin/users_list.html"
    context_object_name = "users"


class DetailAdmin(MongoMixin, DetailView):
    """About the user in the admin model."""
    model = User
    template_name = "admin/user_detail.html"
    context_object_name = "user"

    def post(self, *args, **kwargs):
        """Delete user."""
        self.get_object().delete()
        return redirect("admin:admin-list")
    

def register_admin(request):
    """Attachment of form RegisterForm."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.pop("password")
            user = User(**form.cleaned_data)
            user.set_password(password)
            user.save()
        else:
            messages.error(request, form.errors)
    else:
        form = RegisterForm()
    return render(request, "admin/register_form.html", {"form": form})