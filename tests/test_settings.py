from django.conf import global_settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
DATABASES['other'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
}

INSTALLED_APPS = global_settings.INSTALLED_APPS + [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tests',
]

MIDDLEWARE = global_settings.MIDDLEWARE

SECRET_KEY = 'test_secret_key'
