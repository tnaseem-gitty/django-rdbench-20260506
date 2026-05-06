SECRET_KEY = 'dummy-secret-key'
DEBUG = True
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'testapp',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
