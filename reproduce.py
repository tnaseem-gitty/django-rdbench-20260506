import os
import django
from django.conf import settings
from django.db import models
from django.test import TestCase
from django.db.models import Value

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
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

class SimpleUser(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField()

    class Meta:
        app_label = 'auth'

from django.db import connection

def create_test_db():
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(SimpleUser)

create_test_db()

class TestComposedQueries(TestCase):
    def setUp(self):
        SimpleUser.objects.create(username='user1', email='user1@example.com')
        SimpleUser.objects.create(username='user2', email='user2@example.com')

    def test_values_list_with_union(self):
        qs1 = SimpleUser.objects.all()
        qs2 = SimpleUser.objects.all().annotate(extra=Value('extra'))

        # Original problematic case
        result1 = qs1.union(qs2).values('username', 'email')
        print("Result 1 (should be fixed):", list(result1))

        # Expected fixed case
        result2 = qs1.union(qs2).values('email')
        print("Result 2 (should only contain email):", list(result2))

if __name__ == '__main__':
    import unittest
    unittest.main()
