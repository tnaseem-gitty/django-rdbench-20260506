import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'dummy-secret-key-for-testing'

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'test_app',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

USE_TZ = True
