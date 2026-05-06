SECRET_KEY = 'dummy_secret_key'
DEBUG = True
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'test_project.test_app',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
USE_TZ = True
