import os
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={},
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        USE_TZ=False,
    )

import django
django.setup()

from decimal import Decimal
from django.template.defaultfilters import floatformat

def test_floatformat(value):
    result = floatformat(value, 0)
    print(f"Result for {value}: {result}")

print("Testing with string '0.00':")
test_floatformat('0.00')

print("\nTesting with Decimal('0.00'):")
test_floatformat(Decimal('0.00'))

print("\nTesting with string '1.23':")
test_floatformat('1.23')

print("\nTesting with Decimal('1.23'):")
test_floatformat(Decimal('1.23'))

print("\nScript completed.")
