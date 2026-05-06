import os
import django
from django.core.management import call_command
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')
django.setup()

# Load data into non-default database
try:
    call_command('makemigrations', 'testbug')
    call_command('migrate', 'testbug', database='default')
    call_command('migrate', 'testbug', database='other')
    call_command('loaddata', 'books.json', database='other', format='json')
    print("Data loaded successfully, no errors.")
except Exception as e:
    print(f"Error: {e}")
