from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_recommendation_for_user(sender, instance, created, **kwargs):
    if created:
        from content.models import Recommendations
        Recommendations.objects.create(user=instance)