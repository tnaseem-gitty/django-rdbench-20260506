from datetime import datetime

from django.db.models.functions import TruncDate, TruncTime
from django.test import SimpleTestCase
from django.utils import timezone
import pytz


class DateTimeTruncTests(SimpleTestCase):
    def setUp(self):
        self.naive_datetime = datetime(2022, 1, 1, 12, 30, 45)
        self.ny_tz = pytz.timezone("America/New_York")
        self.aware_datetime = timezone.make_aware(self.naive_datetime, self.ny_tz)

    def test_trunc_date_with_tzinfo(self):
        trunc_date = TruncDate(self.aware_datetime, tzinfo=self.ny_tz)
        self.assertIsInstance(trunc_date, TruncDate)
        self.assertEqual(trunc_date.tzinfo, self.ny_tz)

    def test_trunc_time_with_tzinfo(self):
        trunc_time = TruncTime(self.aware_datetime, tzinfo=self.ny_tz)
        self.assertIsInstance(trunc_time, TruncTime)
        self.assertEqual(trunc_time.tzinfo, self.ny_tz)

    def test_trunc_date_without_tzinfo(self):
        trunc_date = TruncDate(self.naive_datetime)
        self.assertIsInstance(trunc_date, TruncDate)
        self.assertIsNone(trunc_date.tzinfo)

    def test_trunc_time_without_tzinfo(self):
        trunc_time = TruncTime(self.naive_datetime)
        self.assertIsInstance(trunc_time, TruncTime)
        self.assertIsNone(trunc_time.tzinfo)
