import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'django.contrib.gis',
    'django.contrib.postgres',
    'testapp',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SECRET_KEY = 'fake-key'
DEBUG = True
