import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")

import django
django.setup()

from django.core.management import call_command

if __name__ == '__main__':
    call_command('makemigrations', 'test_app', interactive=False)
    call_command('migrate', interactive=False)
    call_command('run_bug_test')
    print("Script completed successfully, no errors.")
