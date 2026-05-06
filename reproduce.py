from uuid import uuid4
from django.db import models
from django.core.management import call_command
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
    'myapp',
    ],
)

django.setup()

class Sample(models.Model):
    name = models.CharField(blank=True, max_length=100)
    class Meta:
        app_label = 'myapp'
# Create the necessary tables
call_command('makemigrations', 'myapp')
call_command('migrate', 'myapp')

Sample.objects.create()
s0 = Sample.objects.create()
s1 = Sample(pk=s0.pk, name='Test 1')
try:
    s1.save()
    print("Script completed successfully, no errors.")
except Exception as e:
    print(f"Error: {e}")
