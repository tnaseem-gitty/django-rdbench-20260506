import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=254, unique=True)

# Configure settings before importing any Django modules
if not settings.configured:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'
    settings.configure(
        DEBUG=True,
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
        ],
        SECRET_KEY='dummy-secret-key',
        AUTH_USER_MODEL='__main__.CustomUser',
    )
    django.setup()

# Now we can import Django modules
from django.test import TestCase
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class AuthenticationFormTest(TestCase):
    def test_username_field_maxlength(self):
        form = AuthenticationForm()
        username_field = form.fields['username']
        widget = username_field.widget
        
        # Check if the maxlength attribute is set in the widget attrs
        self.assertIn('maxlength', widget.attrs)
        
        # Check if the maxlength value is correct
        # The max_length for the username field should now be 254
        self.assertEqual(widget.attrs['maxlength'], '254')

    def test_username_field_renders_maxlength(self):
        form = AuthenticationForm()
        rendered_form = form.as_p()
        
        # Check if the maxlength attribute is present in the rendered HTML
        self.assertIn('maxlength="254"', rendered_form)

if __name__ == '__main__':
    # Run the tests
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=False)
    failures = test_runner.run_tests([__name__])
    sys.exit(bool(failures))
