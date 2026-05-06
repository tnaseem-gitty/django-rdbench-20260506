import os
import unittest

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.project_template.test_settings'

if __name__ == "__main__":
    unittest.TextTestRunner().run(unittest.defaultTestLoader.discover('tests'))
