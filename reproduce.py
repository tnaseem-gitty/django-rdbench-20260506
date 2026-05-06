import os
import django
from django.conf import settings
from django.db import models
from django.db.models import F

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minimal_settings')
django.setup()

from testapp.models import OneModel, TwoModel

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
