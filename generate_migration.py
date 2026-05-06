import os
import django
from django.conf import settings
from django.core.management import call_command

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
django.setup()

call_command('makemigrations', 'test_app', verbosity=2)
