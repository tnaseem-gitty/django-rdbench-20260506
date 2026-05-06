import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.db.models',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TIME_ZONE = 'UTC'
USE_TZ = True
import django
import pytz
from django.conf import settings
from django.db import models
from django.db.models.functions import TruncDate
from django.db.models import Count

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')
django.setup()

class TimeSlots(models.Model):
    start_at = models.DateTimeField()

    class Meta:
        app_label = 'test_app'
tz = pytz.timezone("America/New_York")
report = (
    TimeSlots.objects.annotate(start_date=TruncDate("start_at", tzinfo=tz))
    .values("start_date")
    .annotate(timeslot_count=Count("id"))
    .values("start_date", "timeslot_count")
)

print(report)

