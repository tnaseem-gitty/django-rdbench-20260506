import os
import django
from django.conf import settings
from django.test.utils import get_runner

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(['tests.invalid_models_tests.test_models.OtherModelTests.test_ordering_pointing_to_related_field_pk'])
if failures:
    exit(1)
