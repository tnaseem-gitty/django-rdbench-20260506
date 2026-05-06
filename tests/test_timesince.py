from django.test import TestCase, override_settings
from django.utils.timezone import now
from django.utils.timesince import timesince
from datetime import timedelta

class TimesinceTests(TestCase):
    @override_settings(USE_TZ=True)
    def test_long_interval_with_tz(self):
        current_time = now()
        d = current_time - timedelta(days=31)
        self.assertEqual(timesince(d, current_time), "1\xa0month")

    def test_timesince_future(self):
        current_time = now()
        future_time = current_time + timedelta(days=31)
        self.assertEqual(timesince(future_time, current_time), "0\xa0minutes")

print("Test file created successfully.")
