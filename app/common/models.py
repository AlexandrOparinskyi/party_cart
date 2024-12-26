import uuid

from django.db import models

from app.common.managers import IsActiveManager


class BaseModel(models.Model):
    """
    Custom abstract model with two fields id and is_active

    Fields:
        id (uuid): ID anything
        is_active (bool): Anything is deleted
    """

    id = models.UUIDField(default=uuid.uuid4,
                          unique=True,
                          primary_key=True,
                          db_index=True,
                          editable=False)
    is_active = models.BooleanField(default=True)

    objects = IsActiveManager()

    class Meta:
        abstract = True
