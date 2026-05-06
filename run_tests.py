import os
import django
from django.core.management import call_command

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
django.setup()
call_command('test', 'tests.admin_utils.test_logentry')
