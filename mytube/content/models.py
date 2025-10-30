from django.db import models
from django.contrib.auth import get_user_model

from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary.utils import cloudinary_url

from core.models import UUIDModel


User = get_user_model()


class UserWatchHistoryManager(models.Manager):
    """
    Manager for model UserWatchHistory.

    Has method: add_video.
    """
    def add_video(self, user, video):
        """Get or create model object and returns"""
        history, _ = self.get_or_create(user=user, video=video)
        history.save()
        return history


class UserWatchHistory(UUIDModel):
    """
    Model for recommendations and viewing the viewed.

    Has fields:
    - user
    - video
    - watched_at
    - duration_watched
    - liked
    - is_finished

    Manager is UserWatchHistoryManager

    Method str: returns video title or 'Video deleted'.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, db_index=True)
    video = models.ForeignKey(to="Video", null=True, on_delete=models.SET_NULL, related_name="history")
    watched_at = models.DateTimeField(auto_now_add=True)
    duration_watched = models.PositiveIntegerField(default=0)
    liked = models.BooleanField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)

    objects = UserWatchHistoryManager()

    class Meta:
        unique_together = ["video", "user"]

    def __str__(self):
        return self.video.title if self.video else "Video deleted"
    
    def video_is_finished(self):
        self.is_finished = True
        self.save()
        self.video.views += 1
        self.video.save()
        return self


class AgeLimitChoices(models.TextChoices):
    G = "G", "Gemeral Audience"
    PG13 = "PG-13", "Parents Strongly Cautioned"
    PG15 = "PG-15", "15 nad older"
    NC17 = "NC-17", "Adults Only"


class Video(UUIDModel):
    """
    Model for video.

    Has fields:
    - title
    - description
    - tags
    - views
    - likes
    - age_limit
    - file
    - channel
    - created_at

    Methods 
    - str: returns title
    - user_like and user_dislike: 
      - Checks the status in the viewing history and makes changes
    """
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField("Tag", blank=True, db_index=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.IntegerField(default=0)
    age_limit = models.CharField(max_length=10, choices=AgeLimitChoices.choices, default=AgeLimitChoices.G)
    file = models.FileField(upload_to="videos/", storage=VideoMediaCloudinaryStorage())
    channel = models.ForeignKey(to="channel.Channel", on_delete=models.CASCADE, related_name="videos", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def thumbnail_url(video):
        """
        Returns the URL to a video frame from Cloudinary.
        """
        import os
        from urllib.parse import urlparse

        url_path = urlparse(video.file.url).path  # /video/upload/v1234567890/videos/myvideo.mp4
        public_id = os.path.splitext(url_path.split('/upload/')[1])[0]  # videos/myvideo
        url, _ = cloudinary_url(
            public_id,
            resource_type="video",
            format="jpg",
            start_offset=1
        )
        return url
    
    def user_like(self, user):
        """
        Updates the status of the liked field of the UserWatchHistory model object to true
        and increases the likes field of the current object by 1.

        REQUIRES THE EXISTENCE OF A UserWatchHistory OBJECT FOR THE CURRENT OBJECT AND USER.
        """
        history = UserWatchHistory.objects.get(user=user, video=self)
        if history.liked == False:
            history.liked = True
            history.save()
            self.likes += 2
            self.save()
        elif history.liked == True:
            history.liked = None
            history.save()
            self.likes -= 1
            self.save()
        else:
            history.liked = True
            history.save()
            self.likes += 1
            self.save()

        return self

    def user_dislike(self, user):
        """
        Updates the status of the liked field of the UserWatchHistory model object to False
        and decreases the likes field of the current object by 1.

        REQUIRES THE EXISTENCE OF A UserWatchHistory OBJECT FOR THE CURRENT OBJECT AND USER.
        """
        history = UserWatchHistory.objects.get(user=user, video=self)
        if history.liked == True:
            history.liked = False
            history.save()
            self.likes -= 2
            self.save()
        elif history.liked == False:
            history.liked = None
            history.save()
            self.likes += 1
            self.save()
        else:
            history.liked = False
            history.save()
            self.likes -= 1
            self.save()

        return self


class Tag(models.Model):
    """Model for model Video and recommendations."""
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Recommendations(UUIDModel):
    """
    Specialized repairs for users.

    Has fields:
    - user
    - video
    - update_at

    Method str: returns update_at
    """
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, db_index=True)
    video = models.ManyToManyField(to=Video, blank=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} | {self.update_at.strftime("%d.%m.%Y %H:%M")}"
    

class VideoComment(UUIDModel):
    """
    Video comment model.

    Has fields:
    - author
    - video
    - text
    - created_at

    Method str: returns f"{self.author.username} | {self.video.pk}"
    """
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, db_index=True)
    video = models.ForeignKey(to=Video, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} | {self.video.pk}"