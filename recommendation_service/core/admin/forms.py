from django import forms

from .models import User


class RegisterForm(forms.Form):
    """Form for creating new users has fields ["username", "password"]."""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    class Meta:
        fields = ["username", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects(username=username):
            raise forms.ValidationError("A user with that name already exists.")
        
        return username