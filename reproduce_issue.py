import os
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
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
    django.setup()

from django.db import models

class A(models.Model):
    class Meta:
        abstract = True
        app_label = 'contenttypes'
    myfield = models.IntegerField()

class B(A):
    class Meta:
        app_label = 'contenttypes'

class C(A):
    class Meta:
        app_label = 'contenttypes'

print(len({B._meta.get_field('myfield'), C._meta.get_field('myfield')}))
print(B._meta.get_field('myfield') == C._meta.get_field('myfield'))

print("Script completed successfully, no errors.")
