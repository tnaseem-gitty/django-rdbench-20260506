from django.contrib.sessions.backends.db import SessionStore as db
from django.contrib.sessions.backends.cache import SessionStore as cache
from django.contrib.sessions.backends.cached_db import SessionStore as cache_db
from django.contrib.sessions.backends.file import SessionStore as file
from django.test import TestCase

import os
import shutil
import string
import tempfile
import unittest
from datetime import timedelta
from http import cookies
from pathlib import Path

from django.conf import settings
from django.contrib.sessions.backends.base import UpdateError
from django.contrib.sessions.backends.cache import SessionStore as CacheSession
from django.contrib.sessions.backends.cached_db import (
    SessionStore as CacheDBSession,
)
from django.contrib.sessions.backends.db import SessionStore as DatabaseSession
from django.contrib.sessions.backends.file import SessionStore as FileSession
from django.contrib.sessions.backends.signed_cookies import (
    SessionStore as CookieSession,
)
from django.contrib.sessions.exceptions import InvalidSessionKey
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.models import Session
from django.contrib.sessions.serializers import (
    JSONSerializer, PickleSerializer,
)
from django.core import management
from django.core.cache import caches
from django.core.cache.backends.base import InvalidCacheBackendError
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.http import HttpResponse
from django.test import (
    RequestFactory, TestCase, ignore_warnings, override_settings,
)
from django.utils import timezone

from .models import SessionStore as CustomDatabaseSession


class SessionTestsMixin:
    # This does not inherit from TestCase to avoid any tests being run with this
    # class, which wouldn't work, and to allow different TestCase subclasses to
    # be used.

    backend = None  # subclasses must specify

    def setUp(self):
        self.session = self.backend()

    def tearDown(self):
        # NB: be careful to delete any sessions created; stale sessions fill up
        # the /tmp (with some backends) and eventually overwhelm it after lots
        # of runs (think buildbots)
        self.session.delete()

    def test_new_session(self):
        self.assertIs(self.session.modified, False)
        self.assertIs(self.session.accessed, False)

    def test_get_empty(self):
        self.assertIsNone(self.session.get('cat'))

    def test_store(self):
        self.session['cat'] = "dog"
        self.assertIs(self.session.modified, True)
        self.assertEqual(self.session.pop('cat'), 'dog')

    def test_pop(self):
        self.session['some key'] = 'exists'
        # Need to reset these to pretend we haven't accessed it:
        self.accessed = False
        self.modified = False

        self.assertEqual(self.session.pop('some key'), 'exists')
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, True)
        self.assertIsNone(self.session.get('some key'))

    def test_pop_default(self):
        self.assertEqual(self.session.pop('some key', 'does not exist'),
                         'does not exist')
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, False)

    def test_pop_default_named_argument(self):
        self.assertEqual(self.session.pop('some key', default='does not exist'), 'does not exist')
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, False)

    def test_pop_no_default_keyerror_raised(self):
        with self.assertRaises(KeyError):
            self.session.pop('some key')

    def test_setdefault(self):
        self.assertEqual(self.session.setdefault('foo', 'bar'), 'bar')
        self.assertEqual(self.session.setdefault('foo', 'baz'), 'bar')
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, True)
        self.assertIs(self.session.accessed, True)
        self.assertIs(self.session.modified, True)

    def test_backwards_compatibility(self):
        from django.conf import settings
        from django.core.management import call_command
        from django.contrib.sessions.backends.base import SessionBase
        import json
        
        # Ensure the database table exists for CustomDatabaseSessionTests
        if self.backend.__name__ == 'CustomDatabaseSession':
            call_command('migrate', 'sessions_tests', verbosity=0, interactive=False)
        
        # Create a session with the current format
        session = self.backend()
        session['key'] = 'value'
        
        # Save the session data
        session.save()
        
        # Get the raw encoded data
        if hasattr(session, '_session'):
            raw_data = session._session
        elif hasattr(session, '_session_cache'):
            raw_data = session._session_cache
        else:
            self.fail("Unable to access raw session data")
        
        # Simulate changing DEFAULT_HASHING_ALGORITHM to 'sha1'
        original_algorithm = getattr(settings, 'DEFAULT_HASHING_ALGORITHM', None)
        settings.DEFAULT_HASHING_ALGORITHM = 'sha1'
        
        try:
            # If raw_data is a dict, encode it as JSON
            if isinstance(raw_data, dict):
                raw_data = json.dumps(raw_data).encode('utf-8')
            
            # Try to decode the raw data directly
            decoded_data = SessionBase().decode(raw_data)
            self.assertEqual(decoded_data.get('key'), 'value')
            
            # Load the session using the backend
            loaded_session = self.backend(session.session_key)
            loaded_session.load()
            
            # Check if the data is correctly loaded
            self.assertEqual(loaded_session.get('key'), 'value')
            
            # Modify and save the session with 'sha1' algorithm
            loaded_session['new_key'] = 'new_value'
            loaded_session.save()
            
            # Load the session again to verify the changes
            reloaded_session = self.backend(session.session_key)
            reloaded_session.load()
            
            self.assertEqual(reloaded_session.get('key'), 'value')
            self.assertEqual(reloaded_session.get('new_key'), 'new_value')
        finally:
            # Restore original hashing algorithm
            settings.DEFAULT_HASHING_ALGORITHM = original_algorithm
class DatabaseSessionTests(SessionTestsMixin, TestCase):
    backend = DatabaseSession

class CacheDBSessionTests(SessionTestsMixin, TestCase):
    backend = CacheDBSession

class FileSessionTests(SessionTestsMixin, TestCase):
    backend = FileSession

class CacheSessionTests(SessionTestsMixin, TestCase):
    backend = CacheSession

class CustomDatabaseSessionTests(SessionTestsMixin, TestCase):
class BackwardsCompatibilityTests(TestCase):
    def setUp(self):
        from django.conf import settings
        self.original_algorithm = getattr(settings, 'DEFAULT_HASHING_ALGORITHM', None)
        settings.DEFAULT_HASHING_ALGORITHM = 'sha1'

    def tearDown(self):
        from django.conf import settings
        settings.DEFAULT_HASHING_ALGORITHM = self.original_algorithm

    def test_backwards_compatibility(self):
        from django.contrib.sessions.backends.db import SessionStore
        from django.contrib.sessions.backends.base import SessionBase
        import json

        # Create a session with the current format
        session = SessionStore()
        session['key'] = 'value'
        session.save()

        # Get the raw encoded data
        raw_data = session.session_data

        # Try to decode the raw data directly
        decoded_data = SessionBase().decode(raw_data)
        self.assertEqual(decoded_data.get('key'), 'value')

        # Load the session using the backend
        loaded_session = SessionStore(session.session_key)
        loaded_session.load()

        # Check if the data is correctly loaded
        self.assertEqual(loaded_session.get('key'), 'value')

        # Modify and save the session with 'sha1' algorithm
        loaded_session['new_key'] = 'new_value'
        loaded_session.save()

        # Load the session again to verify the changes
        reloaded_session = SessionStore(session.session_key)
        reloaded_session.load()

        self.assertEqual(reloaded_session.get('key'), 'value')
        self.assertEqual(reloaded_session.get('new_key'), 'new_value')
