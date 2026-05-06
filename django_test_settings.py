DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'test_app',
]

SECRET_KEY = 'fake-key'

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
