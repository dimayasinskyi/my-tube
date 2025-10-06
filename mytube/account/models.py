from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

from cloudinary_storage.storage import MediaCloudinaryStorage


class CountryChoises(models.TextChoices):
    """Model for selecting countries in the CustomUser model."""
    UA = "UA", "Ukraine"
    US = "US", "United States"
    UK = "UK", "United Kingdom"
    DE = "DE", "Germany"
    FR = "FR", "France"
    ES = "ES", "Spain"
    IT = "IT", "Italy"
    PL = "PL", "Poland"
    CN = "CN", "China"
    JP = "JP", "Japan"
    KR = "KR", "South Korea"
    BR = "BR", "Brazil"
    CA = "CA", "Canada"
    AU = "AU", "Australia"


class CustomUser(AbstractUser):
    """
    User model inherited from AbstractUser.
    
    Has fields:
    - avatar
    - country
    - age
    - fields from AbstractUser

    Methods:
    - str: returns full username
    - get_avatar_url: returns url avatar or url default avatar
    """
    avatar = models.ImageField(null=True, blank=True, upload_to="user/avatar/", storage=MediaCloudinaryStorage())
    country = models.CharField(max_length=2, null=True, blank=True, choices=CountryChoises.choices)
    age = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username
    
    def get_avatar_url(self):
        """Returns self.avatar.url or url default avatar"""
        if self.avatar:
            return self.avatar.url
        return static("default/avatar_default.png")
    

    