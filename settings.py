import os
import django
from django.conf import settings
from django.db import models
from django.db.models import Sum, F

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

# Create a simple Book model
class Book(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        app_label = 'test_app'

# Set up the database
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_app_book (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    ''')
    cursor.execute('INSERT INTO test_app_book (id) SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3')

# Reproduce the bug
try:
    result = Book.objects.annotate(idx=F("id")).aggregate(Sum("id", default=0))
    print(f"Result: {result}")
except Exception as e:
    print(f"Error occurred: {str(e)}")

print("Script completed.")
