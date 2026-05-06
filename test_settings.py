
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'tests',
    'tests.db_functions',
]

SECRET_KEY = 'fake-key'
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

