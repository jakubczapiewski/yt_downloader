import uuid

from django.db import models
from model_utils.models import TimeStampedModel


class VideoRequest(TimeStampedModel):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    url = models.CharField(max_length=50)
    resolution = models.CharField(max_length=20, blank=True, default=0)
    size = models.IntegerField(blank=True, default=0)
    progress = models.IntegerField(default=0)
    file_exist = models.BooleanField(default=True)
