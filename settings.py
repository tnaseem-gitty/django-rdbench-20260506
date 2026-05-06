INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'myapp',
]

USE_I18N = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
