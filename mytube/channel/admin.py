from django.contrib import admin

from content.models import Video
from .models import Channel


class VideoInline(admin.TabularInline):
    model = Video
    fields = ["title", "file"]
    extra = 1


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    inlines = [VideoInline]