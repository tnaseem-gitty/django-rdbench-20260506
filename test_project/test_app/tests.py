from django.test import TestCase
from .models import TestModelNoDimensions, TestModelWithDimensions

class ImageFieldTest(TestCase):
    def test_imagefield_signal_connection(self):
        # Create instances to trigger signal connections
        instance_no_dimensions = TestModelNoDimensions()
        instance_with_dimensions = TestModelWithDimensions()

        # Check if the signal is connected for the model with dimensions
        self.assertFalse(hasattr(TestModelNoDimensions, '_image_field_signal_connected'))
        self.assertTrue(hasattr(TestModelWithDimensions, '_image_field_signal_connected'))

        print(f"TestModelNoDimensions signal connected: {hasattr(TestModelNoDimensions, '_image_field_signal_connected')}")
        print(f"TestModelWithDimensions signal connected: {hasattr(TestModelWithDimensions, '_image_field_signal_connected')}")
