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
    """
    The user login form checks:
    - whether all fields have been filled in 
    - whether the user exists 
    - whether the password matches
    
    Returns data without a password.
    """
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

        user = User.objects(username=username).first()
        if not username or not password:
            raise forms.ValidationError("Fill in all fields.")
        elif not user:
            raise forms.ValidationError("Check username not found.")
        elif not user.check_password(password):
            raise forms.ValidationError("The password is incorrect.")
        
        return cleaned_data