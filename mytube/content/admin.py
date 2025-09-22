from django.contrib import admin

from .models import Video, Tag, UserWatchHistory, Recommendations


admin.site.register(Video)
admin.site.register(Tag)
admin.site.register(UserWatchHistory)
admin.site.register(Recommendations)
