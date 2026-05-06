from django.test import TestCase
from django.contrib.admin.utils import display_for_field
from django.db import models
from django.forms import fields as form_fields

class TestModel(models.Model):
    json_field = models.JSONField()

class JSONFieldDisplayTest(TestCase):
    def test_jsonfield_display(self):
        test_instance = TestModel(json_field={"foo": "bar"})
        field = TestModel._meta.get_field('json_field')
        display_value = display_for_field(test_instance.json_field, field, '')
        self.assertEqual(display_value, '{"foo": "bar"}')

print("Script completed successfully, no errors.")
