from django.contrib import admin

from .models import Video, Tag, UserWatchHistory, Recommendations, VideoComment


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    search_fields = ["title"]


admin.site.register(Tag)
admin.site.register(UserWatchHistory)
admin.site.register(Recommendations)
admin.site.register(VideoComment)