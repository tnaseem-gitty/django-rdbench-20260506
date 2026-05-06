import unittest
import os
import sys

# Set the PYTHONPATH to include the current directory and the tests directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'tests')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'tests')))
# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'
if __name__ == "__main__":
    unittest.TextTestRunner().run(unittest.defaultTestLoader.discover('tests/filtered_relation'))
