import os
import django
from django.core.management import call_command
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

try:
    call_command('migrate', 'testapp', '0001')
    call_command('migrate', 'testapp', '0002')
    print("Migrations ran successfully.")
except Exception as e:
    print(f"Error: {e}")
