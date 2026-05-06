import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()
from django.db.models import Count, Case, When, IntegerField
from django.test import TestCase
from tests.aggregation.models import Book

class ReproduceIssueTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.b1 = Book.objects.create(name='Book 1', rating=4.5)
        cls.b2 = Book.objects.create(name='Book 2', rating=3.0)
        cls.b3 = Book.objects.create(name='Book 3', rating=4.0)
        cls.b4 = Book.objects.create(name='Book 4', rating=4.0)

    def test_count_case_distinct(self):
        vals = Book.objects.aggregate(
            count=Count(
                Case(
                    When(rating__gte=4.0, then=1),
                    output_field=IntegerField()
                ),
                distinct=True
            )
        )
        print(vals)

from django.test.utils import get_runner, teardown_test_environment
from django.conf import settings

from django.test.utils import teardown_test_environment

teardown_test_environment()
TestRunner = get_runner(settings)
test_runner = TestRunner()

TestRunner = get_runner(settings)
test_runner = TestRunner()
test_runner.run_tests(["reproduce"])
