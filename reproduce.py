import os
from django.conf import settings
from django.apps import apps
from myapp.models import Item, Status

# Minimal settings configuration
settings.configure(
    USE_I18N=True,
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'myapp',
    ],
)

# Ensure apps are loaded
apps.populate(settings.INSTALLED_APPS)

print("Script completed successfully, no errors.")
