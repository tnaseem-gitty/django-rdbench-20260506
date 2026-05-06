from django.test import TestCase
from django.db.models import Avg, Sum, Min, Max

class AggregateTestCase(TestCase):
    def test_allow_distinct(self):
        self.assertTrue(Avg.allow_distinct)
        self.assertTrue(Sum.allow_distinct)
        self.assertTrue(Min.allow_distinct)
        self.assertTrue(Max.allow_distinct)

if __name__ == '__main__':
    import django
    from django.conf import settings
    settings.configure(DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}})
    django.setup()
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["test_aggregates"])
    print("Test failures:", failures)
