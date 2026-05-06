import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.i18n.sampleproject.settings'
django.setup()

TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(['tests.admin_views.tests.LimitChoicesToInAdminTest.test_limit_choices_to_with_q_object'])
if failures:
    sys.exit(bool(failures))
