import os
import sys
import django
from django.core.management import call_command
from django.db import connection
from django.conf import settings

# Set up a simple Django settings configuration
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
    )

django.setup()

# Create test tables
with connection.cursor() as cursor:
    cursor.execute("CREATE TABLE foo (id INTEGER PRIMARY KEY AUTOINCREMENT, other_id INTEGER UNIQUE)")
    cursor.execute("CREATE TABLE bar (id INTEGER PRIMARY KEY AUTOINCREMENT, other_id INTEGER, FOREIGN KEY(other_id) REFERENCES foo(other_id))")

# Redirect stdout to capture output
from io import StringIO
old_stdout = sys.stdout
sys.stdout = StringIO()

# Run inspectdb command
call_command('inspectdb', 'foo', 'bar', no_color=True)

# Get the output and restore stdout
output = sys.stdout.getvalue()
sys.stdout = old_stdout

print(output)
print("Test completed.")
