import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
django.setup()

from django.db.models import Count
from django.test import TestCase
from testapp.models import Thing, Related
from django.core.management import call_command

# Run migrations
call_command('migrate')

# Define test case
class IssueTestCase(TestCase):
    def setUp(self):
        t = Thing.objects.create()
        for _ in range(2):
            Related.objects.create(thing=t)

    def test_issue(self):
        print("Normal query:")
        print(Thing.objects.annotate(rc=Count('related')).order_by('rc').values('id', 'rc'))

        print("\nQuery with order_by('related'):")
        print(Thing.objects.annotate(rc=Count('related')).order_by('related').values('id', 'rc'))

        print("\nQuery with order_by('?'):")
        print(Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc'))

        print("\nSQL for order_by('?') query:")
        print(Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc').query)

if __name__ == '__main__':
    from django.test.utils import get_runner
    from django.conf import settings
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["__main__"])
    print("\nScript completed successfully, no errors." if failures == 0 else "\nTest failures occurred.")
