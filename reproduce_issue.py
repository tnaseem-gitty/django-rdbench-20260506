from django.conf import settings
from django.db import models
from django.apps import apps
import os

# Configure Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

apps.populate(settings.INSTALLED_APPS)

f = models.CharField(max_length=200)
d = {f: 1}

print(f"Hash of field before assignment: {hash(f)}")

class Book(models.Model):
    title = f
    class Meta:
        app_label = 'myapp'

print(f"Hash of field after assignment: {hash(f)}")

try:
    assert f in d
    print("Test passed: Field is still in the dictionary after being assigned to a model.")
except AssertionError:
    print("Test failed: Field is no longer in the dictionary after being assigned to a model.")

print("Script completed.")
