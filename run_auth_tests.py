import os
import django
from django.conf import settings
from django.test.utils import get_runner, setup_test_environment
from django.db import connections

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'
    settings.configure(
        DEBUG=True,
        SECRET_KEY='dummy_secret_key_for_testing',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.admin',
            'tests.auth_tests',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        MIDDLEWARE=[
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ],
        ROOT_URLCONF='tests.auth_tests.urls',
        MIGRATION_MODULES={},  # Disable migrations
    )
    django.setup()
    
    # Set up the test environment
    setup_test_environment()
    
    # Create the test database
    for connection in connections.all():
        connection.creation.create_test_db()

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=False)
    test_modules = [
        'tests.auth_tests.test_forms',
        'tests.auth_tests.test_views',
        'tests.auth_tests.test_models',
    ]
    failures = test_runner.run_tests(test_modules)
    
    # Destroy the test database
    for connection in connections.all():
        connection.creation.destroy_test_db(verbosity=1)

    print("Test failures:", failures)
