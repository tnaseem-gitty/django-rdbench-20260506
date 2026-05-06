from django.conf import settings
import os

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.admin',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'positions',
        'testapp',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
)

import django
django.setup()

from django.db import models
from positions.fields import PositionField
from django.contrib import admin
from django.core.management import call_command
from testapp.models import Thing
from django.apps import AppConfig

class TestAppConfig(AppConfig):
    name = 'testapp'

@admin.register(Thing)
class ThingAdmin(admin.ModelAdmin):
    list_display = ['number', 'order']

call_command('check')
print("Script completed successfully, no errors.")
