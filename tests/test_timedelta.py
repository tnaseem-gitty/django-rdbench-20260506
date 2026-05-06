from django.test import TestCase
from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta

class TestModel(models.Model):
    td_field = models.DurationField()

    class Meta:
        ordering = ['td_field__pk']
        app_label = 'tests'

class TimeDeltaSerializationTestCase(TestCase):
    def test_timedelta_ordering(self):
        TestModel.objects.create(td_field=timedelta(milliseconds=345))
        TestModel.objects.create(td_field=timedelta(milliseconds=344))
        
        # This should not raise a ValidationError
        try:
            list(TestModel.objects.all())
        except ValidationError:
            self.fail("Ordering by 'td_field__pk' raised ValidationError")
