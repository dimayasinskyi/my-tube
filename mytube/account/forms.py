from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    """Registration form with fields: ["first_name", "last_name", "username", "country", "age", "password1", "password2"]."""
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "placeholder": "Username",
        "class": "w-full border rounded px-3 py-1 mb-2",
    }))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        "placeholder": "Password",
        "class": "w-full border rounded px-3 py-1 mb-2",
    }))
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput(attrs={
        "placeholder": "Repeat password",
        "class": "w-full border rounded px-3 py-1 mb-2",
    }))

    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "username", "country", "age", "password1", "password2"]
        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "First name",
                "class": "w-full border rounded px-3 py-1 mb-2",
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Last name",
                "class": "w-full border rounded px-3 py-1 mb-2",
            }),
            "country": forms.Select(attrs={
                "class": "w-full border rounded px-3 py-1 mb-2",
            }),
            "age": forms.NumberInput(attrs={
                "placeholder": "Age",
                "class": "w-full border rounded px-3 py-1 mb-2",
            }),
        }


class LoginForm(AuthenticationForm):
    """Login form with fields: ["username", "password"]."""
    class Meta:
        model = get_user_model()
        fields = ["username", "password"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget = forms.TextInput(attrs={
            "placeholder": "Username",
            "class": "w-full border rounded px-3 py-2 mb-3",
        })
        self.fields["password"].widget = forms.TextInput(attrs={
            "placeholder": "Password",
            "class": "w-full border rounded px-3 py-2 mb-3",
        })


class ProfileForm(forms.ModelForm):
    """Profile form with fields: ["username", "first_name", "last_name", "country", "age", "avatar"]"""
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "country", "age", "avatar"]
        widgets = {
            "avatar": forms.FileInput(attrs={"id": "avatar-input", "class": "hidden"})
        }
        