INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'testapp',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'test'
