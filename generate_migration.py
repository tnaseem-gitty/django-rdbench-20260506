import django
from django.conf import settings
from django.core.management import call_command
from django.db import models
import os

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.db.migrations',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

django.setup()

class MyField(models.TextField):
    pass

class MyBaseModel(models.Model):
    class Meta:
        abstract = True

class MyMixin:
    pass

    class Meta:
        app_label = 'app'

# Create migration
call_command('makemigrations', 'app')

# Print the generated migration file
migration_file = 'migrations/0001_initial.py'
if os.path.exists(migration_file):
    with open(migration_file, 'r') as file:
        print(file.read())
else:
    print("Migration file not found.")
