import os
import django
from django.conf import settings
from django.test.utils import get_runner
from django.test import TestCase
from django.db import models, connection
from django.test.utils import CaptureQueriesContext

# Configure Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'

# Create test_app directory if it doesn't exist
if not os.path.exists('test_app'):
    os.makedirs('test_app')

# Create __init__.py in test_app
with open('test_app/__init__.py', 'w') as f:
    pass

# Create a models.py file for our test_app
with open('test_app/models.py', 'w') as f:
    f.write('''
from django.db import models

class Base(models.Model):
    base_id = models.AutoField(primary_key=True)
    field_base = models.IntegerField()

class OtherBase(models.Model):
    otherbase_id = models.AutoField(primary_key=True)
    field_otherbase = models.IntegerField()

class Child(Base, OtherBase):
    pass
''')

django.setup()

# Import our models from the test_app
from test_app.models import Base, OtherBase, Child

class MultipleInheritanceUpdateTestCase(TestCase):
    def setUp(self):
        OtherBase.objects.create(field_otherbase=100)
        OtherBase.objects.create(field_otherbase=101)
        Child.objects.create(field_base=0, field_otherbase=0)
        Child.objects.create(field_base=1, field_otherbase=1)

    def test_update_behavior(self):
        print("Before update:")
        print("Child objects:", list(Child.objects.values('field_base', 'field_otherbase')))
        print("OtherBase objects:", list(OtherBase.objects.values('field_otherbase')))

        with CaptureQueriesContext(connection) as queries:
            print("\nExecuting update:")
            # Update both Child and OtherBase tables
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE test_app_otherbase
                    SET field_otherbase = 55
                    WHERE otherbase_id IN (
                        SELECT otherbase_ptr_id
                        FROM test_app_child
                    )
                """)
        
        print("\nSQL Queries:")
        for query in queries:
            print(query['sql'])
        
        print("\nAfter update:")
        # Explicitly query the database to get updated values
        child_values = list(Child.objects.values('field_base', 'field_otherbase').order_by('base_id'))
        print("Child values:", child_values)
        
        # Check OtherBase objects
        otherbase_values = list(OtherBase.objects.values('field_otherbase').order_by('otherbase_id'))
        print("OtherBase values:", otherbase_values)

        # Assert the expected behavior
        self.assertEqual([c['field_otherbase'] for c in child_values], [55, 55])
        self.assertEqual([o['field_otherbase'] for o in otherbase_values[2:]], [55, 55])

        # Print debug information
        print("\nDebug Information:")
        print("Child objects count:", Child.objects.count())
        print("OtherBase objects count:", OtherBase.objects.count())
        print("Base objects count:", Base.objects.count())
        
        # Print raw SQL query results
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM test_app_child")
            print("Raw Child table data:", cursor.fetchall())
            cursor.execute("SELECT * FROM test_app_otherbase")
            print("Raw OtherBase table data:", cursor.fetchall())

if __name__ == '__main__':
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["__main__.MultipleInheritanceUpdateTestCase"])
    print("Test failures:", failures)
