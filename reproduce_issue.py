import os
import django
from django.db import models
from django.test import TestCase

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.test_sqlite")
django.setup()

class Item(models.Model):
    uid = models.AutoField(primary_key=True, editable=False)
    f = models.BooleanField(default=False)

    def reset(self):
        self.uid = None
        self.f = False

class Derived(Item):
    pass

class SaveTestCase(TestCase):
    def setUp(self):
        self.derived = Derived.objects.create(f=True)  # create the first object
        item = Item.objects.get(pk=self.derived.pk)
        obj1 = item.derived
        obj1.reset()
        obj1.save()  # the first object is overwritten

    def test_f_true(self):
        obj = Item.objects.get(pk=self.derived.pk)
        self.assertTrue(obj.f)

if __name__ == '__main__':
    import unittest
    unittest.main()

print("Script completed successfully, no errors.")
