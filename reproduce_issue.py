import os
import django
from django.conf import settings

# Set up minimal Django settings
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
    TIME_ZONE='UTC',
)
django.setup()

# Now we can import and use Django utilities
import datetime
from django.utils import dateformat

test_date = datetime.datetime(123, 4, 5, 6, 7)
formatted_date = dateformat.format(test_date, "y")
print(f"Django dateformat: {formatted_date}")

python_formatted = test_date.strftime("%y")
print(f"Python strftime: {python_formatted}")

print("Expected output: 23")
print("Script completed successfully, no errors.")
