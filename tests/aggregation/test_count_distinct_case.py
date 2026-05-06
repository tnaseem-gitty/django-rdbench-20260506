from django.db.models import Case, Count, When, Value, IntegerField
from django.test import TestCase
from django.contrib.auth.models import User

class CountDistinctCaseTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.bulk_create([
            User(username='user1', is_active=True, is_staff=False),
            User(username='user2', is_active=True, is_staff=False),
            User(username='user3', is_active=False, is_staff=False),
            User(username='user4', is_active=True, is_staff=True),
        ])

    def test_count_distinct_case_single_value(self):
        query = User.objects.aggregate(
            active_count=Count(
                Case(
                    When(is_active=True, then=Value(1)),
                    output_field=IntegerField(),
                ),
                distinct=True
            )
        )
        print(f"Single value query result: {query}")
        self.assertEqual(query['active_count'], 1)

    def test_count_distinct_case_multiple_values(self):
        query = User.objects.aggregate(
            status_count=Count(
                Case(
                    When(is_active=True, is_staff=False, then=Value(1)),
                    When(is_active=True, is_staff=True, then=Value(2)),
                    When(is_active=False, then=Value(3)),
                    output_field=IntegerField(),
                ),
                distinct=True
            )
        )
        print(f"Multiple values query result: {query}")
        self.assertEqual(query['status_count'], 3)
