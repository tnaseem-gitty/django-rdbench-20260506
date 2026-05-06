import sys
from django.utils import autoreload

if __name__ == "__main__":
    autoreload.run_with_reloader(lambda: __import__("test_module"))
