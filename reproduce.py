import django
from django.conf import settings
from django.db import models

# Minimal settings configuration
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'test_app',  # Register the current module as an app
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

django.setup()

class MyIntWrapper(int):
    def __new__(cls, value):
        return super().__new__(cls, value)

class MyAutoField(models.BigAutoField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return MyIntWrapper(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return int(value)

class AutoModel(models.Model):
    class Meta:
        app_label = 'test_app'
# Create the table
from django.core.management import call_command
call_command('makemigrations', 'test_app')
call_command('migrate')

# Reproduce the issue
am = AutoModel.objects.create()
print(type(am.id))  # Expected: <class '__main__.MyIntWrapper'>, Actual: <class 'int'>

ams = [AutoModel()]
AutoModel.objects.bulk_create(ams)
print(type(ams[0].id))  # Expected: <class '__main__.MyIntWrapper'>, Actual: <class 'int'>
