import os
import sys

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_sqlite'
    test_dir = os.path.dirname(__file__)
    sys.path.insert(0, test_dir)
    
    from tests.runtests import setup, django_tests
    
    setup(verbosity=1, test_labels=[], parallel=1, start_at=None, start_after=None)
    failures = django_tests(verbosity=1, interactive=True, failfast=False, test_labels=[])
    sys.exit(bool(failures))
