from django.test import TestCase
from django.db import models
from django.db.models import F
import datetime

class Experiment(models.Model):
    estimated_time = models.DurationField()

    class Meta:
        app_label = 'auth'

class TimeDeltaTest(TestCase):
    def setUp(self):
        Experiment.objects.create(estimated_time=datetime.timedelta(milliseconds=345))

    def test_timedelta_annotation(self):
        delta = datetime.timedelta(days=1)
        result = list(Experiment.objects.annotate(duration=F('estimated_time') + delta))

        expected = datetime.timedelta(days=1, milliseconds=345)
        self.assertEqual(result[0].duration, expected)

        print(f"Result: {result[0].duration}")
        print(f"Expected: {expected}")
        print(f"Are they equal? {result[0].duration == expected}")

# This will allow the test to be discovered by Django's test runner
__test__ = {'TimeDeltaTest': TimeDeltaTest}
