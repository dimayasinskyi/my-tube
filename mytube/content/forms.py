from django.forms import ModelForm

from .models import Video


class VideoCreateForm(ModelForm):
    class Meta:
        model = Video
        fields = ["title", "description","file"]