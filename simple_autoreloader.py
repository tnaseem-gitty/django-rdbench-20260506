import sys
import os
import subprocess
import importlib

def get_child_arguments():
    args = [sys.executable]
    main_module = sys.modules['__main__']
    if getattr(main_module, '__spec__', None) is not None:
        if main_module.__spec__.parent:
            args += ['-m', main_module.__spec__.parent]
        else:
            args += ['-m', main_module.__spec__.name]
    else:
        args += [sys.argv[0]]
    args += sys.argv[1:]
    return args

def restart_with_reloader():
    new_environ = {**os.environ, "SIMPLE_AUTORELOAD_ENV": "true"}
    args = get_child_arguments()
    return subprocess.call(args, env=new_environ, close_fds=False)

def run_with_reloader(main_func):
    if os.environ.get("SIMPLE_AUTORELOAD_ENV") == "true":
        main_func()
    else:
        while True:
            exit_code = restart_with_reloader()
            if exit_code != 3:
                return exit_code

if __name__ == "__main__":
    # Simulate running with python -m
    sys.argv = ['-m', 'test_module']
    run_with_reloader(lambda: importlib.import_module("test_module"))
