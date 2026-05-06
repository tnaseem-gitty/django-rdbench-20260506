import os
import django
from django.conf import settings
from django.test.utils import get_runner

settings.configure(
    SECRET_KEY='dummy_secret_key',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'tests.messages_tests',
    ],
)
django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(['tests/messages_tests'])
if failures:
    exit(1)
