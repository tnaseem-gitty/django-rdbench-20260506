import uuid
from django.conf import settings
from django.core.management import execute_from_command_line

print("Configuring settings...")
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            '__main__',  # This current module
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        DEFAULT_AUTO_FIELD='django.db.models.AutoField',
    )

import django
django.setup()

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Foo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        app_label = '__main__'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Bar(models.Model):
    foo_content_type = models.ForeignKey(
        ContentType, related_name='actor',
        on_delete=models.CASCADE, db_index=True
    )
    foo_object_id = models.CharField(max_length=255, db_index=True)
    foo = GenericForeignKey('foo_content_type', 'foo_object_id')

    class Meta:
        app_label = '__main__'
    foo_content_type = models.ForeignKey(
        ContentType, related_name='actor',
        on_delete=models.CASCADE, db_index=True
    )
    foo_object_id = models.CharField(max_length=255, db_index=True)
    foo = GenericForeignKey('foo_content_type', 'foo_object_id')

import os
import sys
from django.core.management import call_command

# Create and apply migrations
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__main__')
call_command('makemigrations', 'contenttypes')
call_command('makemigrations', '__main__')
call_command('migrate')
def reproduce_issue():
    execute_from_command_line(['manage.py', 'migrate'])
    foo_instance = Foo.objects.create()
    Bar.objects.create(foo_content_type=ContentType.objects.get_for_model(Foo), foo_object_id=foo_instance.id)
    queryset = Bar.objects.all().prefetch_related('foo')
    for bar in queryset:
        print(bar.foo)  # This should not be None if prefetch_related works correctly

if __name__ == "__main__":
    reproduce_issue()
