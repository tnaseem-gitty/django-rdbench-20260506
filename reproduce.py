import django
from django.conf import settings
from django.db import models

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'test1',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

if __name__ == "__main__":
    django.setup()
    
    from test1.models import Outer, A, Thing
        
    from django.core.management import call_command
    call_command('makemigrations', 'test1')
# Removed duplicate lines
