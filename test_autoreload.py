import sys
import os
from django.utils.autoreload import get_child_arguments

def test_get_child_arguments():
    # Save the original sys.argv and current working directory
    original_argv = sys.argv
    original_cwd = os.getcwd()

    # Change to the directory containing autoreload.py
    os.chdir('/django__django/django/utils')

    # Test case 1: Normal execution (using autoreload.py)
    sys.argv = ['autoreload.py', 'arg1', 'arg2']
    args = get_child_arguments()
    print("Test case 1 (Normal execution):")
    print(f"Input: {sys.argv}")
    print(f"Output: {args}")
    print()

    # Test case 2: Execution with -m (package)
    sys.argv = ['-m', 'django.utils.autoreload', 'arg1', 'arg2']
    args = get_child_arguments()
    print("Test case 2 (Execution with -m package):")
    print(f"Input: {sys.argv}")
    print(f"Output: {args}")
    print()

    # Test case 3: Execution with -m (module)
    sys.argv = ['-m', 'autoreload', 'arg1', 'arg2']
    args = get_child_arguments()
    print("Test case 3 (Execution with -m module):")
    print(f"Input: {sys.argv}")
    print(f"Output: {args}")
    print()

    # Restore the original sys.argv and working directory
    sys.argv = original_argv
    os.chdir(original_cwd)

if __name__ == '__main__':
    test_get_child_arguments()
