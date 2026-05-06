import os
import django
from django.test import TestCase
from django.apps import AppConfig

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")

class TestAppConfig(AppConfig):
    name = 'test_app'

django.setup()

from test_models import TestModelNoDimensions, TestModelWithDimensions

class ImageFieldTest(TestCase):
    def test_imagefield_no_dimensions(self):
        instance = TestModelNoDimensions()
        self.assertFalse(hasattr(instance, '_post_init_signal'))

    def test_imagefield_with_dimensions(self):
        instance = TestModelWithDimensions()
        self.assertTrue(hasattr(instance, '_post_init_signal'))

if __name__ == '__main__':
    import unittest
    unittest.main()
