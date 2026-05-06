INSTALLED_APPS = [
    'test_app',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db.sqlite3',
    }
}
SECRET_KEY = 'dummy'
