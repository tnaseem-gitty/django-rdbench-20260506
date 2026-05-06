from django.contrib.admin.utils import display_for_field
from django.db import models
from django.test import TestCase, override_settings

class JSONFieldModel(models.Model):
    data = models.JSONField()

    class Meta:
        app_label = 'admin_utils'

@override_settings(INSTALLED_APPS=['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'tests.admin_utils'])
class JSONFieldAdminTest(TestCase):
    def test_jsonfield_display(self):
        field = JSONFieldModel._meta.get_field('data')
        test_value = {"foo": "bar"}
        result = display_for_field(test_value, field, '')
        self.assertEqual(result, '{"foo": "bar"}')

        # Test with None value
        result = display_for_field(None, field, '')
        self.assertEqual(result, '')

        # Test with invalid JSON
        invalid_json = {"foo": set()}  # set is not JSON serializable
        result = display_for_field(invalid_json, field, '')
        self.assertIn("Invalid JSON", result)
