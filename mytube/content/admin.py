from django.contrib import admin

from .models import Video, Tag, VideoComment


class VideoCommentInline(admin.TabularInline):
    model = VideoComment
    extra = 0


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    inlines = [VideoCommentInline]


class VideoTagInline(admin.TabularInline):
    model = Video.tags.through
    extra = 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    inlines = [VideoTagInline]