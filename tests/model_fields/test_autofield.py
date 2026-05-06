from django.db import models
from django.test import TestCase

class MyBigAutoField(models.BigAutoField):
    pass

class AutoFieldSubclassTests(TestCase):
    def test_bigautofield_subclass(self):
        self.assertTrue(issubclass(MyBigAutoField, models.AutoField))

    def test_smallautofield_subclass(self):
        class MySmallAutoField(models.SmallAutoField):
            pass
        self.assertTrue(issubclass(MySmallAutoField, models.AutoField))

    def test_autofield_subclass(self):
        class MyAutoField(models.AutoField):
            pass
        self.assertTrue(issubclass(MyAutoField, models.AutoField))
