
import os
import django
from django.test.runner import DiscoverRunner

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
django.setup()

test_runner = DiscoverRunner(verbosity=2, interactive=False)
failures = test_runner.run_tests(['django.tests.expressions'])
exit(failures)

