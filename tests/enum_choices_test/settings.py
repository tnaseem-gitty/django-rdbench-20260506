SECRET_KEY = 'dummy'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'tests.enum_test_app',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
USE_TZ = True
