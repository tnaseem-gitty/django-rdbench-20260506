import os
import django
from django.core.management import call_command

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_sqlite'
    django.setup()
    call_command('test', 'tests.forms_tests.widget_tests.test_bound_widget', verbosity=2)
