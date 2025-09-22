from django.conf import settings
from rest_framework import serializers

import requests

from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    video_id = serializers.IntegerField(source="id")
    is_liked_by_user = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    duration_watched = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ["video_id", "views", "likes", "tags", "duration_watched", "is_liked_by_user"] 

    def get_tags(self, obj):
        return [tag.title for tag in obj.tags.all()]
    
    def get_duration_watched(self, obj):
        first_history = obj.history.first()
        return first_history.duration_watched if first_history else 0
              

    def get_is_liked_by_user(self, obj):
        user = self.context.get("user")
        first_history = obj.history.first()
        duration = first_history.duration_watched if first_history else 0
        data = {
            "user_id": user.id,
            "video_id": obj.id,
            "duration_watched": duration,
            "views": obj.views,
            "likes": obj.likes,
            "tags": [tag.title for tag in obj.tags.all()],
            "country": user.country or "UA",
            }
        response = requests.post(settings.RECOMMENDATION_SERVICE_URL, json=data)
        return response.json()