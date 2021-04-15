from django.db import models
from common.models import BaseModel
from django.conf import settings
from .constants import CHOICES_PRIORITY_TASKS


class Tag(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="tag")
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "tag"


class Task(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="task")
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, blank=True)
    description = models.TextField()
    priority = models.CharField(max_length=100, choices=CHOICES_PRIORITY_TASKS)
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = "task"
