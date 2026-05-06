import os
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    # Set up a minimal Django settings configuration
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        ROOT_URLCONF='',
        MIDDLEWARE=[],
    )

    django.setup()

    # Get the test runner
    TestRunner = get_runner(settings)

    # Run the test
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests.test_migration_loader"])

    if failures:
        print("Test failed")
    else:
        print("Test passed successfully")
