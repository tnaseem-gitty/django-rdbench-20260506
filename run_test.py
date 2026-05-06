import os
import django
from django.conf import settings
from django.test.utils import get_runner

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_sqlite'
django.setup()

TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(["tests.utils_tests.test_dateformat.DateFormatTests.test_year_less_than_1000"])

print("Test failures:", failures)
