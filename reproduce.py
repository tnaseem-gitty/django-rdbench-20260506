import os
import django
from django.conf import settings
from django.db import models

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        '__main__',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

django.setup()

class Readable(models.Model):
    title = models.CharField(max_length=200)

class Readable(models.Model):
    pass

class Book(Readable):
    title = models.CharField(max_length=200)

if __name__ == "__main__":
    from django.core.management import call_command
    call_command('makemigrations')
    call_command('migrate')

