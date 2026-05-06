import os
import sys
import unittest

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from django.conf import settings
from django.test import TestCase
from django.apps import apps

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
    )

import django
django.setup()

class ClearCacheTests(TestCase):
    def test_clear_cache_clears_swappable_settings_name(self):
        # Call get_swappable_settings_name to populate the cache
        result1 = apps.get_swappable_settings_name('auth.User')
        self.assertEqual(result1, 'AUTH_USER_MODEL')
        
        cache_info1 = apps.get_swappable_settings_name.cache_info()
        self.assertEqual(cache_info1.hits, 0)
        self.assertEqual(cache_info1.misses, 1)
        self.assertEqual(cache_info1.currsize, 1)
        
        # Call again to hit the cache
        result2 = apps.get_swappable_settings_name('auth.User')
        self.assertEqual(result2, 'AUTH_USER_MODEL')
        
        cache_info2 = apps.get_swappable_settings_name.cache_info()
        self.assertEqual(cache_info2.hits, 1)
        self.assertEqual(cache_info2.misses, 1)
        self.assertEqual(cache_info2.currsize, 1)
        
        # Clear the cache
        apps.clear_cache()
        
        # Verify that the cache is cleared
        cache_info_after = apps.get_swappable_settings_name.cache_info()
        self.assertEqual(cache_info_after.hits, 0)
        self.assertEqual(cache_info_after.misses, 0)
        self.assertEqual(cache_info_after.currsize, 0)

if __name__ == '__main__':
    unittest.main()
