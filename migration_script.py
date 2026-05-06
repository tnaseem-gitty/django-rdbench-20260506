import os
import django
from django.core.management import call_command

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')
django.setup()

# Create and apply migrations
call_command('makemigrations', 'test_app')
call_command('migrate', 'test_app')
