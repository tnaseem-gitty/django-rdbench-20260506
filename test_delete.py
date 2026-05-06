import os
import django
from django.conf import settings
from django.db import models, connection
from django.db.models.deletion import Collector
from django.test.utils import CaptureQueriesContext

# Minimal Django settings configuration
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'main.apps.MainConfig',  # This allows the models in this script to be recognized
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)
from django.core.management import call_command

# Setup Django
django.setup()

# Run migrations to create the necessary tables
call_command('makemigrations', 'main')
call_command('migrate')

from main.models import Person, User, Entry

# Create test data
user = User.objects.create()
entry1 = Entry.objects.create(created_by=user, updated_by=user)
entry2 = Entry.objects.create(created_by=user, updated_by=user)
person = Person.objects.create()
person.friends.add(person)

# Capture the SQL queries
with CaptureQueriesContext(connection) as context:
    collector = Collector(using='default')
    collector.collect([user])
    collector.delete()

    # Print the executed queries
    for query in context.captured_queries:
        print(query['sql'])

print("Script completed successfully, no errors.")

print("Script completed successfully, no errors.")
