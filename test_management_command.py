import sys
from django.core.management import call_command

if __name__ == "__main__":
    print("Running without --skip-checks:")
    call_command('test_skip_checks')

    print("\nRunning with --skip-checks:")
    call_command('test_skip_checks', skip_checks=True)
