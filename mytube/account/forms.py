from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "country", "age"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "country", "age", "avatar"]
        widgets = {
            "avatar": forms.FileInput(attrs={"id": "avatar-input", "class": "hidden"})
        }
        