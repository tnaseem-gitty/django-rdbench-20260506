import os
import django
from django.conf import settings
from django.db import models, connection
from django.apps import AppConfig, apps

# Configure Django settings
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        '__main__',
    ],
    DEBUG=True,  # Enable debug mode to capture SQL queries
)

# Define AppConfig
class MyAppConfig(AppConfig):
    name = '__main__'
    verbose_name = "My App"

# Register the AppConfig
apps.populate(settings.INSTALLED_APPS)

# Set up Django
django.setup()

# Define a simple model
class TestModel(models.Model):
    name = models.CharField(max_length=100)

# Create the table
with connection.schema_editor() as schema_editor:
    schema_editor.create_model(TestModel)

# Populate the table with data
TestModel.objects.bulk_create([TestModel(name=f'Item {i}') for i in range(100)])

# Perform the delete operation and print the generated SQL
with connection.cursor() as cursor:
    TestModel.objects.all().delete()
    print(connection.queries[-1]['sql'])

print("Script completed successfully, no errors.")

