DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
    'other': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'other_db.sqlite3',
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'testbug',
    'testbug',
]

ROOT_URLCONF = 'testbug.urls'

SECRET_KEY = 'dummy_secret_key'
