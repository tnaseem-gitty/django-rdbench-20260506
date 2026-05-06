import os
import django
from django.conf import settings
from django.test.utils import setup_test_environment
from django.test.runner import DiscoverRunner

# Configure Django settings
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',  # Use an in-memory database for testing
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'tests',
        ],
        USE_TZ=True,
    )

django.setup()
setup_test_environment()

runner = DiscoverRunner(verbosity=2, interactive=False)
suite = runner.test_suite()
specific_test = runner.test_loader.loadTestsFromName('tests.migrations.test_autodetector.AutodetectorTests.test_move_field_to_subclass')
suite.addTest(specific_test)
result = runner.run_suite(suite)

print("Test execution completed.")
exit(not result.wasSuccessful())
