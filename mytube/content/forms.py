from django import forms

from .models import Video


class VideoCreateForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "description", "tags", "file"]
        widgets = {
            "file": forms.FileInput(attrs={
                "accept": "video/*",
                "class": "block w-full border rounded px-3 py-2 focus:outline-none foring-red-300",
            }),
            "title": forms.TextInput(attrs={
                "placeholder": "Enter video title",
                "class": "block w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:ring-red-300",
                }),
            "description": forms.Textarea(attrs={
                "rows": "4",
                "placeholder": "Enter video description",
                "class": "block w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:ring-red-300",
            }),
            "tags": forms.SelectMultiple(attrs={
                "class": "block w-full border rounded px-3 py-2 focus:outline-none focus:ring focus:ring-red-300"
            })
        }