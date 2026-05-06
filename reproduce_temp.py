import pytz
from django.db import models
from django.db.models.functions import TruncDate
from django.db.models import Count

class TimeSlots(models.Model):
    start_at = models.DateTimeField()

tz = pytz.timezone("America/New_York")
report = (
    TimeSlots.objects.annotate(start_date=TruncDate("start_at", tzinfo=tz))
    .values("start_date")
    .annotate(timeslot_count=Count("id"))
    .values("start_date", "timeslot_count")
)

print(report)
