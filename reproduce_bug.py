import os
import unittest
from django.conf import settings
from django.apps import AppConfig

class TestsConfig(AppConfig):
    name = 'tests'
    label = 'tests'

# Set up Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'reproduce_bug_settings'

if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'tests',
        ],
    )

import django
django.setup()

from django.db import models, connection
from django.db.models import Sum
import pickle

# Define the model
class Toy(models.Model):
    name = models.CharField(max_length=16)
    material = models.CharField(max_length=16)
    price = models.PositiveIntegerField()

    class Meta:
        app_label = 'tests'

# Create the database table
with connection.schema_editor() as schema_editor:
    schema_editor.create_model(Toy)

class ReproduceBugTest(unittest.TestCase):
    def setUp(self):
        # Create some sample data
        Toy.objects.create(name='foo', price=10, material='wood')
        Toy.objects.create(name='bar', price=20, material='plastic')
        Toy.objects.create(name='baz', price=100, material='wood')

    def test_reproduce_bug(self):
        # Original query
        prices = Toy.objects.values('material').annotate(total_price=Sum('price'))
        print("Original query result:")
        print(list(prices))
        print("Type of first item in original query:", type(list(prices)[0]))

        # Pickle and unpickle the query
        pickled_query = pickle.dumps(prices.query)
        print("\nPickled query:", pickled_query)
        
        unpickled_query = pickle.loads(pickled_query)
        print("\nUnpickled query:", unpickled_query)
        
        prices2 = Toy.objects.all()
        prices2.query = unpickled_query

        print("\nAfter pickling and unpickling:")
        print("Query:", prices2.query)
        print("SQL:", prices2.query.sql_with_params())
        
        try:
            result = list(prices2)
            print("Unpickled query result:")
            print(result)
            print("Type of first item in unpickled query:", type(result[0]))
        except Exception as e:
            print(f"Error occurred: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()

        # Try to recreate the original query without pickling
        prices3 = Toy.objects.values('material').annotate(total_price=Sum('price'))
        print("\nRecreated query without pickling:")
        print(list(prices3))

if __name__ == '__main__':
    unittest.main()
