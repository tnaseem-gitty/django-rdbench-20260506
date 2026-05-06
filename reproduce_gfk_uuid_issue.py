import os
import django
from django.conf import settings

def setup_django():
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
            ],
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            USE_TZ=True,
        )
    django.setup()

setup_django()

import unittest
from django.core.management import call_command
from django.db import connection
import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

class Foo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'contenttypes'

class Bar(models.Model):
    foo_content_type = models.ForeignKey(
        ContentType, related_name='actor',
        on_delete=models.CASCADE, db_index=True
    )
    foo_object_id = models.CharField(max_length=255, db_index=True)
    foo = GenericForeignKey('foo_content_type', 'foo_object_id')
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'contenttypes'

def create_custom_models():
    call_command('migrate')
    # Create tables for our custom models
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(Foo)
        schema_editor.create_model(Bar)

create_custom_models()

class TestGFKUUIDIssue(TestCase):
    def setUp(self):
        self.foo = Foo.objects.create(name="Test Foo")
        self.bar = Bar.objects.create(
            foo_content_type=ContentType.objects.get_for_model(Foo),
            foo_object_id=str(self.foo.id),
            name="Test Bar"
        )

    def test_prefetch_related(self):
        # First, verify that the relationship works without prefetch_related
        bar_without_prefetch = Bar.objects.first()
        print(f"Without prefetch_related:")
        print(f"Bar name: {bar_without_prefetch.name}")
        print(f"Foo name: {bar_without_prefetch.foo.name if bar_without_prefetch.foo else 'None'}")
        
        # Now test with prefetch_related
        bar_with_prefetch = Bar.objects.all().prefetch_related('foo').first()
        print(f"\nWith prefetch_related:")
        print(f"Bar name: {bar_with_prefetch.name}")
        print(f"Foo name: {bar_with_prefetch.foo.name if bar_with_prefetch.foo else 'None'}")
        
        # Assert that both methods return the same result
        self.assertEqual(bar_without_prefetch.foo, bar_with_prefetch.foo)
        self.assertEqual(bar_without_prefetch.foo.name, bar_with_prefetch.foo.name)
        self.assertEqual(bar_without_prefetch.foo.id, bar_with_prefetch.foo.id)
        
        # Check if the prefetch_related actually prefetched the related object
        with self.assertNumQueries(0):
            _ = bar_with_prefetch.foo

if __name__ == '__main__':
    unittest.main(verbosity=2)
