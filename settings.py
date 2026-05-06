import os
import django
from django.conf import settings
from django.db import models
from django.db.models import F

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

class OneModel(models.Model):
    class Meta:
        ordering = ("-id",)
    id = models.BigAutoField(primary_key=True)
    root = models.ForeignKey("OneModel", on_delete=models.CASCADE, null=True)
    oneval = models.BigIntegerField(null=True)

class TwoModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    record = models.ForeignKey(OneModel, on_delete=models.CASCADE)
    twoval = models.BigIntegerField(null=True)

# Reproducing the issue
qs = TwoModel.objects.filter(record__oneval__in=[1,2,3])
qs = qs.order_by("record__root_id")
print(qs.query)

qs = TwoModel.objects.filter(record__oneval__in=[1,2,3])
qs = qs.order_by("record__root__id")
print(qs.query)

qs = TwoModel.objects.filter(record__oneval__in=[1,2,3])
qs = qs.annotate(root_id=F("record__root_id"))
qs = qs.order_by("root_id")
print(qs.query)

qs = TwoModel.objects.filter(record__oneval__in=[1,2,3])
qs = qs.order_by("-record__root_id")
print(qs.query)

print("Script completed successfully, no errors.")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SECRET_KEY = 'dummy_secret_key_for_testing'
DEBUG = True
