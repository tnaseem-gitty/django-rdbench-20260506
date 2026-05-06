import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

call_command('makemigrations', 'main', interactive=False)
