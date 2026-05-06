import os
import django
from django.core.management import call_command

# Set up Django environment
from django.conf import settings

# Set up Django environment
settings.configure(SECRET_KEY='temporary_secret_key', DEBUG=True)
django.setup()

# Run the cycle_data management command
try:
    call_command('cycle_data', '--sleep-time=0')
    print("Script completed successfully, no errors.")
except Exception as e:
    print(f"Error: {e}")
