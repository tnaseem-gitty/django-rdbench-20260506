import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'dummy-secret-key-for-tests'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'test_app',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
