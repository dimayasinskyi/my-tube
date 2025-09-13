from django.db import models
from django.contrib.auth import get_user_model
from django.templatetags.static import static


User = get_user_model()


class Channel(models.Model):
    """
    To highlight users who create videos.

    Has fields:
    - author
    - poenitization
    - created_at

    Methods:
    - str: returns name
    - get_avatar_url: url avatar or url avatar user or default url avatar
    - get_banner_url: url banner or default url banner
    """
    name = models.CharField(max_length=100)
    avatar = models.FileField(null=True, blank=True, upload_to="channel/avatar/")
    banner = models.FileField(null=True, blank=True,upload_to="channel/banner/")
    author = models.OneToOneField(to=User, on_delete=models.CASCADE)
    poenitization = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        if self.author.avatar:
            return self.author.avatar.url
        return static("default/avatar_default.png")
    
    def get_banner_url(self):
        if self.banner:
            return self.banner.url
        return static("default/banner_default.png")