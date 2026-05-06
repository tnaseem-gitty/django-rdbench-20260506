from django.db import models
from django.test import TestCase
from django.core.files.storage import default_storage, Storage

class CustomStorage(Storage):
    def _save(self, name, content):
        return name

    def _open(self, name, mode='rb'):
        return None

    def exists(self, name):
        return False

def get_storage():
    return CustomStorage()

class FileFieldDeconstructTest(TestCase):
    def test_deconstruct_with_callable_storage(self):
        field = models.FileField(storage=get_storage)
        name, path, args, kwargs = field.deconstruct()
        
        self.assertIn('storage', kwargs)
        self.assertEqual(kwargs['storage'], get_storage)
        
        # Ensure that the storage is not instantiated
        self.assertTrue(callable(kwargs['storage']))

    def test_deconstruct_with_default_storage(self):
        field = models.FileField()
        name, path, args, kwargs = field.deconstruct()
        
        self.assertNotIn('storage', kwargs)

    def test_deconstruct_with_instance_storage(self):
        field = models.FileField(storage=CustomStorage())
        name, path, args, kwargs = field.deconstruct()
        
        self.assertIn('storage', kwargs)
        self.assertIsInstance(kwargs['storage'], CustomStorage)
        self.assertFalse(callable(kwargs['storage']))

