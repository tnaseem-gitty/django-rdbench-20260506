from django.db import models
from datetime import timedelta

class TestModel(models.Model):
    td_field = models.DurationField()

    class Meta:
        ordering = ['td_field']  # This is valid ordering
    td_field = models.DurationField()

    class Meta:
        ordering = ['td_field']  # This should be valid
