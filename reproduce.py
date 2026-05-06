import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')

from django.db import models
from django.db.models import Count
from django.core.management import execute_from_command_line

# Run migrations
execute_from_command_line(['manage.py', 'migrate'])

from models import Thing, Related
# Create data
t = Thing.objects.create()
rs = [Related.objects.create(thing=t) for _ in range(2)]

# Queries to reproduce the issue
print(Thing.objects.annotate(rc=Count('related')).order_by('rc').values('id', 'rc'))
print(Thing.objects.annotate(rc=Count('related')).order_by('related').values('id', 'rc'))
print(Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc'))
print(Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc').query)
