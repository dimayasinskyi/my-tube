from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_recommendation_for_user(sender, instance, created, **kwargs):
    """When creating a user, it creates a recommendation model for them."""
    if created:
        from content.models import Recommendations, Video
        Recommendations.objects.create(user=instance).video.set(Video.objects.order_by("?")[:50])