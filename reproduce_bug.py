import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")

from django.conf import settings
from django.core.management import call_command
import django

if __name__ == '__main__':
    # Add our app to INSTALLED_APPS
    settings.INSTALLED_APPS += ['reproduce_bug']

    # Setup Django
    django.setup()

    # Create a migration for our model
    call_command('makemigrations', 'reproduce_bug')

    # Apply all migrations
    call_command('migrate')

    # Run the test
    from reproduce_bug.models import AutoFieldTestCase
    test_case = AutoFieldTestCase()
    test_case._pre_setup()
    test_case.test_auto_field_conversion()
    test_case._post_teardown()
    
    print("Script completed successfully, no errors.")
