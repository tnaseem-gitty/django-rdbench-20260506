SECRET_KEY = 'dummy'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'test_app',
]

# Add this line to silence Django's system check warnings
SILENCED_SYSTEM_CHECKS = ['models.E001']
