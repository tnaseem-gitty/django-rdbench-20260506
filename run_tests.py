import os
import django
from django.core.management import call_command

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
django.setup()
import unittest
unittest.TextTestRunner().run(unittest.defaultTestLoader.discover('tests.admin_views.tests'))
