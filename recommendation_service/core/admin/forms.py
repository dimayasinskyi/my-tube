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
    

class LoginForm(forms.Form):

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

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.pop("password")

        if not User.objects(username=username):
            raise forms.ValidationError("A user with that name already exists.")
        elif not User.objects(username=username).first().check_password(password):
            raise forms.ValidationError("The password is incorrect.")
        
        return cleaned_data