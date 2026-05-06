import uuid
import django
from django.conf import settings
from django.db import models, connection
from django.db.models import Count
from django.test import TransactionTestCase
from django.test.runner import DiscoverRunner

# Configure Django settings
settings.configure(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    INSTALLED_APPS=['__main__'],
)
django.setup()

class CustomQuerySet(models.QuerySet):
    @property
    def ordered(self):
        """
        Returns True if the QuerySet is ordered -- i.e. has an order_by()
        clause or a default ordering on the model, and no GROUP BY clause.
        """
        if self.query.group_by:
            # If there's a GROUP BY, it's only ordered if there's an explicit order_by
            return bool(self.query.order_by)
        elif self.query.extra_order_by or self.query.order_by:
            return True
        elif self.query.default_ordering and self.query.get_meta().ordering:
            return True
        else:
            return False

class Foo(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)

    objects = CustomQuerySet.as_manager()

    class Meta:
        ordering = ['name']

class QuerySetOrderedTest(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print("Running setUpClass")
        
        # Manually create the table
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE __main___foo (
                    uuid CHAR(32) PRIMARY KEY,
                    name VARCHAR(100)
                )
            ''')
        
        # Check if the table exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='__main___foo';")
            result = cursor.fetchone()
            print(f"Table __main___foo exists: {result is not None}")

    def setUp(self):
        super().setUp()
        print("Running setUp")
        Foo.objects.create(name='B')
        Foo.objects.create(name='A')
        Foo.objects.create(name='C')

    def test_ordered_property(self):
        print("Running test_ordered_property")
        qs = Foo.objects.all()
        print("qs.ordered:", qs.ordered)
        print("qs.query.default_ordering:", qs.query.default_ordering)
        print("SQL:", qs.query)

        qs2 = Foo.objects.annotate(Count("pk")).all()
        print("\nqs2.ordered:", qs2.ordered)
        print("qs2.query.default_ordering:", qs2.query.default_ordering)
        print("SQL:", qs2.query)

if __name__ == '__main__':
    test_runner = DiscoverRunner(verbosity=2, interactive=False)
    test_runner.setup_test_environment()
    old_config = test_runner.setup_databases()
    
    try:
        test_suite = test_runner.test_suite()
        test_suite.addTest(QuerySetOrderedTest('test_ordered_property'))
        result = test_runner.run_suite(test_suite)
    finally:
        test_runner.teardown_databases(old_config)
        test_runner.teardown_test_environment()

    print("\nScript completed successfully, no errors.")
