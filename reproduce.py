import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
from django.db.models import F
from models import SelfRef

django.setup()

o = SelfRef.objects.all().first()
o.c8 = F('name')  # model has char fields 'c8' and 'name'
SelfRef.objects.bulk_update([o], ['c8'])

o.refresh_from_db()
print(o.c8)

from django.db import connection
print(connection.queries[-2])
