from django.db import connections
from django.db.migrations.recorder import MigrationRecorder
from django.test import TestCase

class Router:
    def allow_migrate(self, db, model):
        if db == 'default':
            return True
        return False

class MigrationRecorderTest(TestCase):
    databases = {'default', 'other'}

    def setUp(self):
        self.router = Router()
        self.default_connection = connections['default']
        self.other_connection = connections['other']
        self.default_recorder = MigrationRecorder(self.default_connection)
        self.other_recorder = MigrationRecorder(self.other_connection)

    def test_record_applied(self):
        self.default_recorder.record_applied('app', '0001_initial')
        self.assertTrue(self.default_recorder.migration_qs.filter(app='app', name='0001_initial').exists())
        self.other_recorder.record_applied('app', '0001_initial')
        self.assertFalse(self.other_recorder.migration_qs.filter(app='app', name='0001_initial').exists())

    def test_record_unapplied(self):
        self.default_recorder.record_applied('app', '0001_initial')
        self.default_recorder.record_unapplied('app', '0001_initial')
        self.assertFalse(self.default_recorder.migration_qs.filter(app='app', name='0001_initial').exists())
        self.other_recorder.record_applied('app', '0001_initial')
        self.other_recorder.record_unapplied('app', '0001_initial')
        self.assertFalse(self.other_recorder.migration_qs.filter(app='app', name='0001_initial').exists())

if __name__ == "__main__":
    import django
    from django.conf import settings
    from django.test.utils import get_runner
    import sys

    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
            'other': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'django.db.migrations',
        ],
    )
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["__main__"])
    if failures:
        sys.exit(bool(failures))
