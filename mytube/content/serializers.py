from rest_framework import serializers

from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    video_id = serializers.IntegerField(source="id")
    duration_watched = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ["user_id", "video_id", "duration_watched", "views", "likes", "tags", "country"] 

    def get_user_id(self, obj):
        user = self.context.get("user")
        return user.id

    def get_tags(self, obj):
        return [tag.title for tag in obj.tags.all()]
    
    def get_duration_watched(self, obj):
        first_history = obj.history.first()
        return first_history.duration_watched if first_history else 0
    
    def get_country(self, obj):
        user = self.context.get("user")
        return user.country or "UA"