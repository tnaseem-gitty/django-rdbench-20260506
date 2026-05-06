import sys
import types
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments():
    # Simulate running with `-m django`
    sys.argv = ['runserver']
    main_spec = types.ModuleType('__main__')
    main_spec.__spec__ = types.SimpleNamespace(parent='django')
    sys.modules['__main__'] = main_spec
    args = get_child_arguments()
    assert '-m' in args and 'django' in args
    print("Test passed for `-m django`")

    # Simulate running with a script
    sys.argv = ['manage.py', 'runserver']
    args = get_child_arguments()
    assert 'manage.py' in args
    print("Test passed for script")

if __name__ == "__main__":
    test_get_child_arguments()
    print("All tests passed.")
