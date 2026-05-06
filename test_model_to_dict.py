from django.test import TestCase
from django.db import models
from django.forms.models import model_to_dict

class ModelToDictTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        class TestModel(models.Model):
            field1 = models.CharField(max_length=100)
            field2 = models.IntegerField()

            class Meta:
                app_label = 'test_model_to_dict'

        cls.TestModel = TestModel

    def test_model_to_dict_empty_fields(self):
        instance = self.TestModel(field1="test", field2=42)
        result = model_to_dict(instance, fields=[])
        self.assertEqual(result, {}, "model_to_dict with empty fields list should return an empty dict")

    def test_model_to_dict_none_fields(self):
        instance = self.TestModel(field1="test", field2=42)
        result = model_to_dict(instance, fields=None)
        self.assertIn('field1', result, "model_to_dict with fields=None should include all fields")
        self.assertIn('field2', result, "model_to_dict with fields=None should include all fields")
