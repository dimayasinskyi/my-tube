from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from core.mongo_sessions_backend import collection
from ..mixins import MongoMixin
from .models import User
from .forms import RegisterForm, LoginForm


class ListAdmin(MongoMixin, ListView):
    """List of users in the admin panel."""
    model = User
    template_name = "admin/users_list.html"
    context_object_name = "users"


class DetailAdmin(LoginRequiredMixin, MongoMixin, DetailView):
    """About the user in the admin model."""
    model = User
    template_name = "admin/user_detail.html"
    context_object_name = "user"

    def post(self, *args, **kwargs):
        """Delete user or create, update token."""
        user = self.get_object()
        if "delete" in self.request.POST:
            collection.delete_many({"user_id": str(self.request.user.id)})
            user.delete()
            return redirect("admin:admin-list")
        elif "create_token" in self.request.POST:
            user.create_token()
        return redirect(self.request.path)
    

def register_admin(request):
    """Stores the user ID in the session and creates it and attachment of form RegisterForm."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.pop("password")
            user = User(**form.cleaned_data)
            user.set_password(password)
            user.save()
            request.session["user_id"] = str(user.id)
            request.session.create()
            return redirect("admin:admin-list")
    else:
        form = RegisterForm()
    return render(request, "admin/register_form.html", {"form": form})


def login_in(request):
    """Stores the user ID in the session and creates or updates it and attachment of form LoginForm."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects(**form.cleaned_data).first()
            request.session["user_id"] = str(user.id)
            request.session.create_or_save(session_key=request.session.get("session_key"))
            return redirect("admin:admin-list")
    else:
        form = LoginForm()

    return render(request, "admin/login_form.html", {"form": form})


@login_required()
def logout(request):
    """Deletes the session."""
    if request.user.is_authenticated:
        request.session.flush()
        return redirect("admin:admin-list")