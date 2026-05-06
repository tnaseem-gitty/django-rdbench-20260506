INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    '__main__',  # This will include the models defined in the script
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Use an in-memory database for testing
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
