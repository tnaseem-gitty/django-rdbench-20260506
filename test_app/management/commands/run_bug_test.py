from django.core.management.base import BaseCommand
from django.db import connection, models
from django.test import TestCase
from test_app.models import MyModel

class Command(BaseCommand):
    help = 'Run the bug reproduction test'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys = OFF;')

        class BugReproductionTest(TestCase):
            def test_exists_subquery_with_empty_queryset(self, stdout):
                qs = MyModel.objects.filter(~models.Exists(MyModel.objects.none()), name='test')
                stdout.write(f"QuerySet: {qs}")
                try:
                    stdout.write(f"SQL Query: {qs.query}")
                except Exception as e:
                    stdout.write(f"Exception raised: {type(e).__name__}")
                    # Force SQL compilation even if exception is raised
                    compiler = qs.query.get_compiler(using=qs.db)
                    stdout.write(f"Forced SQL Query: {compiler.as_sql()[0]}")

        test = BugReproductionTest()
        test.setUp()
        test.test_exists_subquery_with_empty_queryset(self.stdout)

        with connection.cursor() as cursor:
            cursor.execute('PRAGMA foreign_keys = ON;')

        self.stdout.write(self.style.SUCCESS('Bug reproduction test completed successfully'))
