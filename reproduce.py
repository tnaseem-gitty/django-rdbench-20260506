import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.auth_tests.settings'
django.setup()

from django.db import models
from tests.base.models import MyModel

qs = MyModel.objects.filter(~models.Exists(MyModel.objects.none()), name='test')
print(qs)
print(qs.query)
