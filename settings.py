import django
from django.conf import settings

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'tests',
        'django.contrib.admin',
        'django.contrib.sites',
    ],
    SECRET_KEY='test_secret_key',
    DEFAULT_AUTO_FIELD='django.db.models.AutoField',
)

django.setup()
