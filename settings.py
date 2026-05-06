INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'models',  # Add our models module
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'dummy'
