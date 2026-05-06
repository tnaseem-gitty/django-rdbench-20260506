SECRET_KEY = 'dummy'
DEBUG = True
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'tests.migrations',  # Add this line
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
