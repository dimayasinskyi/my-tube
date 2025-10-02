from django import forms

from .models import Channel


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ["name", "avatar", "banner", "poenitization"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "block w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:ring-red-300"}),
            "avatar": forms.FileInput(attrs={"id": "avatar-input", "class": "hidden"}),
            "banner": forms.FileInput(attrs={"id": "banner-input", "class": "hidden"}),
        }