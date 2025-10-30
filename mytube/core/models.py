import uuid
from django.db import models


class UUIDModel(models.Model):
    """Model to replace the standard ID with uuid."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True