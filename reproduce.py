import os
import django
from django.conf import settings
from django.db import models
from django.core.management import call_command

# Configure settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'myapp.apps.MyappConfig',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

django.setup()

from myapp.models import Article

# Create the table
call_command('makemigrations', 'myapp')
call_command('migrate')

# Try to use in_bulk with the unique constraint
try:
    Article.objects.in_bulk(field_name="slug")
except ValueError as e:
    print(e)
