import os
import django
from django.conf import settings
from django.db import models, connection
from django.db.models import Sum, F

# Set up Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[],
    )
    django.setup()

# Create a simple Book model
class Book(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        app_label = 'reproduce_bug'
        managed = False

# Create the table manually
with connection.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reproduce_bug_book (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    ''')
    cursor.execute('INSERT INTO reproduce_bug_book (id) SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3')

# Reproduce the bug
try:
    result = Book.objects.annotate(idx=F("id")).aggregate(Sum("id", default=0))
    print(f"Result: {result}")
except Exception as e:
    print(f"Error occurred: {str(e)}")

print("Script completed.")
