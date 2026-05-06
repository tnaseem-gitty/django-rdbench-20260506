import os
import django
from django.db import models
from django.test import TestCase

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
django.setup()

class OurModel(models.Model):
    our_field = models.JSONField()

class JSONFieldInLookupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        OurModel.objects.create(our_field={"key": 0})
        OurModel.objects.create(our_field={"key": 1})
        OurModel.objects.create(our_field={"key": 2})

    def test_in_lookup(self):
        first_filter = {'our_field__key__in': [0]}
        first_items = OurModel.objects.filter(**first_filter)
        print(f"Items with __in lookup: {len(first_items)}")

        second_filter = {'our_field__key': 0}
        second_items = OurModel.objects.filter(**second_filter)
        print(f"Items with direct lookup: {len(second_items)}")

        assert len(first_items) == len(second_items), "The __in lookup is not working as expected"

if __name__ == '__main__':
    from django.core.management import call_command
    call_command('migrate')
    
    print("Running the test...")
    test = JSONFieldInLookupTest()
    test.setUpTestData()
    test.test_in_lookup()
    print("Test completed.")
