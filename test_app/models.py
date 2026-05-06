import os
import django
from django.conf import settings
from django.apps import AppConfig, apps
from django.core.management import call_command
from django.db import models
from django.contrib import admin
from django.contrib.admin import site
from django.test import RequestFactory
from test_app.models import RelatedModel, MainModel

# Minimal settings configuration
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.admin',
        'test_app',  # This allows the test models to be recognized
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    USE_I18N=True,
    USE_L10N=True,
    USE_TZ=True,
)

# Define a test app config
class TestAppConfig(AppConfig):
    name = 'test_app'
    label = 'test_app'

# Register the test app config
apps.populate(settings.INSTALLED_APPS)

# Setup Django
django.setup()

# Create and apply migrations for the test models
call_command('makemigrations', 'test_app')
call_command('migrate', 'test_app')

# Define test ModelAdmin
class RelatedModelAdmin(admin.ModelAdmin):
    pass

class MainModelAdmin(admin.ModelAdmin):
    list_filter = ('related',)

# Register models with admin site
site.register(RelatedModel, RelatedModelAdmin)
site.register(MainModel, MainModelAdmin)

# Create test data
related1 = RelatedModel.objects.create(name='B')
related2 = RelatedModel.objects.create(name='A')
MainModel.objects.create(related=related1)
MainModel.objects.create(related=related2)

# Create a request factory
request = RequestFactory().get('/admin/app/mainmodel/')

# Get the model admin instance
model_admin = site._registry[MainModel]

# Get the list filter instance
list_filter = model_admin.get_list_filter(request)[0]

# Check the ordering of the choices
choices = list(list_filter.field_choices(list_filter.field, request, model_admin))
print([choice[1] for choice in choices])  # Should print ['A', 'B']

print("Script completed successfully, no errors.")

