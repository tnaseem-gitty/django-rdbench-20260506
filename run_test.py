import os
from django.conf import settings

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'
    
    settings.configure(
        DEBUG=True,
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'test_app',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
    )
    
    import django
    django.setup()
    
    # Run migrations
    from django.core.management import call_command
    import os
    import shutil

    print("Current working directory:", os.getcwd())
    print("Contents of test_app directory:", os.listdir('test_app'))
    
    print("Contents of test_deferred_fields.py:")
    with open(os.path.join('test_app', 'test_deferred_fields.py'), 'r') as f:
        print(f.read())
    
    # Remove existing migrations
    migrations_dir = os.path.join('test_app', 'migrations')
    if os.path.exists(migrations_dir):
        shutil.rmtree(migrations_dir)
    os.makedirs(migrations_dir)
    open(os.path.join(migrations_dir, '__init__.py'), 'a').close()
    
    print("Running makemigrations...")
    call_command('makemigrations', 'test_app', verbosity=3)
    print("Running migrate...")
    call_command('migrate', verbosity=3)
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False)
    failures = test_runner.run_tests(["test_app.test_deferred_fields"])
    print("Test failures:", failures)
