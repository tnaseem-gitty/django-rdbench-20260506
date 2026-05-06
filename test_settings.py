INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.db',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'test'
