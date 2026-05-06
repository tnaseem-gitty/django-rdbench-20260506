import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'
    django.setup()
    execute_from_command_line(['manage.py', 'test', 'django.contrib.auth'])
