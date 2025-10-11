from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Recommendations


@receiver(m2m_changed, sender=Recommendations.video.through)
def update_timestamp_on_videos_changed(sender, instance, **kwargs):
    """Updates updated_at every time the Video <-> Recommendations relationship changes."""
    instance.save(update_fields=["update_at"])