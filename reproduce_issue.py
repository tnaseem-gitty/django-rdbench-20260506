import os
import django
from django.conf import settings
import uuid
import unittest

# Set up Django configuration
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
    )
    django.setup()

from django.db import models, connection
from django.test import TestCase
from django.test.runner import DiscoverRunner

class Sample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(blank=True, max_length=100)

    class Meta:
        app_label = 'test_app'

    def save(self, *args, **kwargs):
        try:
            existing = Sample.objects.get(pk=self.pk)
            for field in self._meta.fields:
                if field.name != 'id':
                    setattr(existing, field.name, getattr(self, field.name))
            super(Sample, existing).save(*args, **kwargs)
        except Sample.DoesNotExist:
            super().save(*args, **kwargs)
class IssueTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE test_app_sample (
                    id CHAR(32) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL
                )
            ''')

    def test_issue(self):
        s0 = Sample.objects.create()
        s1 = Sample(pk=s0.pk, name='Test 1')
        
        print("Before save:")
        print(f"s0 id: {s0.id}, name: {s0.name}")
        print(f"s1 id: {s1.id}, name: {s1.name}")
        
        s1.save()
        
        print("\nAfter save:")
        print(f"s0 id: {s0.id}, name: {s0.name}")
        print(f"s1 id: {s1.id}, name: {s1.name}")
        
        # Refresh from database
        s0.refresh_from_db()
        s1.refresh_from_db()
        
        print("\nAfter refresh from database:")
        print(f"s0 id: {s0.id}, name: {s0.name}")
        print(f"s1 id: {s1.id}, name: {s1.name}")

    @classmethod
    def tearDownClass(cls):
        with connection.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS test_app_sample')
        super().tearDownClass()

class CustomTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        suite = unittest.TestLoader().loadTestsFromTestCase(IssueTestCase)
        result = self.run_suite(suite)
        return self.suite_result(suite, result)

if __name__ == '__main__':
    runner = CustomTestRunner()
    runner.run_tests([])
