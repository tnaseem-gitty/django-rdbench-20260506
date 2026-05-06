INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'main',  # Add the app label here
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

SECRET_KEY = 'dummy'
