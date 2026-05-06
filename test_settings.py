SECRET_KEY = 'dummy_secret_key'
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'tests',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
USE_TZ = False
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
