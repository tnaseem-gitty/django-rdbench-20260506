SECRET_KEY = 'dummy_secret_key'
DEBUG = True
INSTALLED_APPS = [
    'test_app',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
