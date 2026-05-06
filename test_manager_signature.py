import os
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    settings.configure(
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
        INSTALLED_APPS=['django.contrib.contenttypes', 'django.contrib.auth'],
        DEFAULT_AUTO_FIELD='django.db.models.AutoField',
    )
    django.setup()

from django.test import TestCase
from django.db import models
import inspect

class Person(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        # Use a fake app_label that doesn't need to be in INSTALLED_APPS
        app_label = 'test_models'

class TestManagerSignature(TestCase):
    def test_bulk_create_signature(self):
        signature = inspect.signature(Person.objects.bulk_create)
        parameters = list(signature.parameters.keys())
        self.assertEqual(parameters[:3], ['objs', 'batch_size', 'ignore_conflicts'])
        print("Test passed: bulk_create signature is correct")
        print(f"Full signature: {signature}")

if __name__ == '__main__':
    from django.test.utils import setup_test_environment
    setup_test_environment()
    test_case = TestManagerSignature()
    test_case.test_bulk_create_signature()
