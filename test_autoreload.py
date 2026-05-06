import sys
from django.utils.autoreload import get_child_arguments

def main():
    print("Original sys.argv:", sys.argv)
    child_args = get_child_arguments()
    print("Child arguments:", child_args)

if __name__ == "__main__":
    main()
