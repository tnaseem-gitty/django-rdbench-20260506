import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.auth_tests.settings')
os.environ.setdefault('SECRET_KEY', 'temporary_secret_key')
django.setup()

try:
    call_command('makemigrations')
except Exception as e:
    print(f"Error: {e}")
