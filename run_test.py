
import os
import django
from django.test.utils import setup_databases, teardown_databases
from django.test.runner import DiscoverRunner
from django.apps import apps

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
django.setup()

from tests.db_functions.math.test_mod import ModTests

if __name__ == '__main__':
    runner = DiscoverRunner(verbosity=2, interactive=False)
    old_config = runner.setup_databases()
    
    try:
        # Ensure the models are set up correctly
        apps.get_app_config('db_functions').import_models()
        
        test = ModTests('test_decimal_and_integer')
        result = test.run()
        if result.wasSuccessful():
            print('Test passed successfully!')
        else:
            print('Test failed.')
            print(result.errors)
            print(result.failures)
    finally:
        runner.teardown_databases(old_config)

