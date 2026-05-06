import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_bulk_update.test_settings'
django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(['test_bulk_update'])
if failures:
    exit(1)
