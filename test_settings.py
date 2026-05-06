SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'test_model_to_dict',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
