INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'app',  # Assuming 'app' is the name of the app containing the model
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Use an in-memory database for testing
    }
}

SECRET_KEY = 'test_secret_key'
