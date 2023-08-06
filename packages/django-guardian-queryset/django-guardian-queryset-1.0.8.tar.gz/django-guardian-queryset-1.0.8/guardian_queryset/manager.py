from django.db.models.manager import BaseManager
from guardian_queryset.queryset import GuardianQuerySet
from django.db import models

class GuardianManager(BaseManager.from_queryset(GuardianQuerySet), models.Manager):
    pass


