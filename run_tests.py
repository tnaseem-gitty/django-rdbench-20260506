import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

# Add the parent directory to sys.path to allow importing Django modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == "__main__":
    # Configure minimal settings
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'tests.model_forms',
        ),
        ROOT_URLCONF='tests.urls',
        MIDDLEWARE=[],
    )

    django.setup()

    # Import our test case
    from tests.model_forms.tests import ModelFormFactoryCallbackTests

    # Create a test suite with our test case
    import unittest
    suite = unittest.TestLoader().loadTestsFromTestCase(ModelFormFactoryCallbackTests)

    # Get the test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)

    # Run the tests
    failures = test_runner.run_suite(suite)

    sys.exit(bool(failures))
