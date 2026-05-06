import os
import django
from django.conf import settings

if __name__ == "__main__":
    # Set up the Django environment
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
    
    django.setup()

    from django.test.utils import get_runner

    # Get the test runner
    TestRunner = get_runner(settings)

    # Run the tests
    test_runner = TestRunner(verbosity=1, interactive=False)
    failures = test_runner.run_tests(["django.db.backends.postgresql"])

    # Exit with non-zero status if there were failures
    exit(bool(failures))
