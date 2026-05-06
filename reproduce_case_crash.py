import os
import django
from django.db.models import Case, When, Value, BooleanField, Q
from django.conf import settings
import logging

# Set up logging
logging.basicConfig()
logging.getLogger('django.db.backends').setLevel(logging.DEBUG)

# Set up Django environment
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
        ],
    )
django.setup()

from django.contrib.auth.models import User

# Reproduce the issue
try:
    query = User.objects.annotate(
        _a=Case(
            When(~Q(pk__in=[]), then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
    ).order_by("-_a").values("pk")
    
    # Print the generated SQL
    print("Generated SQL:")
    print(query.query)
    
    # Force query execution
    result = list(query)
    print(f"Query result: {result}")
    print("Query executed successfully.")
except Exception as e:
    print(f"Error occurred: {e}")

print("Script completed.")
