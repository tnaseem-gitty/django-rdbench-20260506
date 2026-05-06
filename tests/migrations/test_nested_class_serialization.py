import os
import sys
import django
from django.db import models
from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test.runner import DiscoverRunner
from django.db.migrations.serializer import serializer_factory
from django.conf import settings

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestNestedClassSerialization(TestCase):
    def test_nested_class_method_serialization(self):
        class TestModel(models.Model):
            class Capability(models.TextChoices):
                BASIC = "BASIC", "Basic"
                PROFESSIONAL = "PROFESSIONAL", "Professional"

                @classmethod
                def default(cls):
                    return [cls.BASIC]

            capabilities = models.JSONField(default=Capability.default)

        # Get the capabilities field
        capabilities_field = TestModel._meta.get_field('capabilities')

        # Create a serializer for the field's default value
        serializer = serializer_factory(capabilities_field.default)

        # Attempt to serialize the default value
        serialized, imports = serializer.serialize()

        # Check if the serialized string correctly references the nested class method
        expected = "tests.migrations.test_nested_class_serialization.TestModel.Capability.default"
        self.assertIn(expected, serialized)

        # Ensure the serialized string can be evaluated
        scope = {}
        exec(f"from django.db import models\n{imports.pop()}\ndef function(): return {serialized}", scope)
        result = scope['function']()

        # Check if the result matches the expected default value
        self.assertEqual(result, ["BASIC"])

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.migrations.test_settings')
    django.setup()
    runner = DiscoverRunner(verbosity=2, interactive=True)
    failures = runner.run_tests(['tests.migrations.test_nested_class_serialization'])
    exit(bool(failures))
