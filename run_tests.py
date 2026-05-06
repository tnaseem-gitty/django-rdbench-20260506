import django
from django.conf import settings
from django.test.utils import get_runner

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'tests.schema',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(['tests.schema.tests.SchemaTests.test_func_unique_constraint_lookups'])
if failures:
    exit(1)
