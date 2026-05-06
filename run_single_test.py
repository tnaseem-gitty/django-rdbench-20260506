import os
import django
from django.conf import settings
from django.test.utils import get_runner

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
django.setup()

from tests.bulk_create.tests import BulkCreateTests

TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(['tests.bulk_create.tests.BulkCreateTests.test_batch_size_compatibility'])
if failures:
    exit(1)
