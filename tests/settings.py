DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

USE_TZ = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
]
from django.conf import settings
from django.apps import apps

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    USE_TZ=True,
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
)

apps.populate(settings.INSTALLED_APPS)
