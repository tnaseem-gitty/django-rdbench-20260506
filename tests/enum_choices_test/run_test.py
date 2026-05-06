import os
import django
from django.conf import settings
from django.test.runner import DiscoverRunner

class NoMigrationTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        pass

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.enum_choices_test.settings'
    django.setup()
    test_runner = NoMigrationTestRunner(verbosity=1, interactive=False)
    print("Running tests...")
    failures = test_runner.run_tests(["tests.test_enum_choices"])
    print(f"Test failures: {failures}")
