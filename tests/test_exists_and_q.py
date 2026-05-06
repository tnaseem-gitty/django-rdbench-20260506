import os
import unittest
from django.conf import settings
from django.db.models import Q
from django.test import SimpleTestCase
from django.db.models.expressions import Exists, RawSQL

# Set up minimal Django settings
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[],
    )

import django
django.setup()

class ExistsAndQTest(SimpleTestCase):
    def test_exists_and_q_commutative(self):
        # Create a simple Exists object
        exists = Exists(RawSQL("SELECT 1", []))

        # Create a simple Q object
        q = Q(id=1)

        # Test Exists & Q
        result1 = exists & q

        # Test Q & Exists
        result2 = q & exists

        # Check if the results are equal
        self.assertEqual(str(result1), str(result2))

        # Check if both results are instances of Q
        self.assertIsInstance(result1, Q)
        self.assertIsInstance(result2, Q)

        # Check if both results contain the Exists object and the original Q object
        self.assertEqual(len(result1.children), 2)
        self.assertEqual(len(result2.children), 2)
        self.assertIn(exists, result1.children)
        self.assertIn(q, result1.children)
        self.assertIn(exists, result2.children)
        self.assertIn(q, result2.children)

        # Check if the connectors are the same
        self.assertEqual(result1.connector, result2.connector)

        print("All tests passed successfully.")

if __name__ == '__main__':
    unittest.main()
