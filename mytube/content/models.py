from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class AgeLimitChoices(models.TextChoices):
    G = "G", "Gemeral Audience"
    PG13 = "PG-13", "Parents Strongly Cautioned"
    PG15 = "PG-15", "15 nad older"
    NC17 = "NC-17", "Adults Only"


class Video(models.Model):
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

    Method str returns title
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.ManyToManyField("Tag", blank=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.IntegerField(default=0)
    age_limit = models.CharField(max_length=10, choices=AgeLimitChoices.choices, default=AgeLimitChoices.G)
    file = models.FileField(upload_to="videos/")
    channel = models.ForeignKey(to="channel.Channel", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Model for model Video and recommendations."""
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class UserWatchHistory(models.Model):
    """
    Model for recommendations and viewing the viewed.

    Has fields:
    - user
    - video
    - watched_at
    - duration_watched
    - is_finished

    Method str: returns video title.
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    video = models.ForeignKey(to=Video, null=True, on_delete=models.SET_NULL)
    watched_at = models.DateTimeField(auto_now_add=True)
    duration_watched = models.PositiveIntegerField(default=0)
    is_finished = models.BooleanField(default=False)

    class Meta:
        unique_together = ["video", "user"]

    def __str__(self):
        return self.video.title


class Recommendations(models.Model):
    """
    Specialized repairs for users.

    Has fields:
    - user
    - video
    - created_at

    Method str: returns created_at
    """
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    video = models.ForeignKey(to=Video, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_at