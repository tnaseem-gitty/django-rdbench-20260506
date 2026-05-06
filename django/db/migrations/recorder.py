from django.apps.registry import Apps
from django.db import DatabaseError, models
from django.utils.functional import classproperty
from django.utils.timezone import now
from django.db import router
from .exceptions import MigrationSchemaMissing


class MigrationRecorder:
    _migration_class = None
    """
    Deal with storing migration records in the database.
    Because this table is actually itself used for dealing with model
    creation, it's the one thing we can't do normally via migrations.
    We manually handle table creation/schema updating (using schema backend)
    and then have a floating model to do queries with.

    If a migration is unapplied its row is removed from the table. Having
    a row in the table always means a migration is applied.
    """
    def __init__(self, connection):
        self.migration_qs = self.Migration.objects.using(self.connection.alias).order_by("app", "name")
    @classproperty
    def Migration(cls):
        """        Lazy load to avoid AppRegistryNotReady if installed apps import
        MigrationRecorder.
        """
        if cls._migration_class is None:
            class Migration(models.Model):
                app = models.CharField(max_length=255)
                name = models.CharField(max_length=255)
                applied = models.DateTimeField(default=now)
            cls._migration_class = Migration
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
        DATABASE_ROUTERS=['__main__.Router'],
    )
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["__main__"])
    if failures:
        sys.exit(bool(failures))

    def ensure_schema(self):
        """Ensure the table exists and has the correct schema."""        # If the table's there, that's fine - we've never changed its schema
        # in the codebase.
        if self.has_table():
            return
        # Check the router
        if not router.allow_migrate(self.connection.alias, self.Migration):
            return
        # Make the table
        try:
            with self.connection.schema_editor() as editor:                editor.create_model(self.Migration)
        except DatabaseError as exc:
            raise MigrationSchemaMissing("Unable to create the django_migrations table (%s)" % exc)

    def applied_migrations(self):
        """
        Return a dict mapping (app_name, migration_name) to Migration instances
        for all applied migrations.
        """
        if self.has_table():
            return {(migration.app, migration.name): migration for migration in self.migration_qs}
        else:
            # If the django_migrations table doesn't exist, then no migrations
            # are applied.
            return {}
    def record_applied(self, app, name):
        """Record that a migration was applied."""
        print(f"Checking allow_migrate for db: {self.connection.alias}, model: {self.Migration}")
        if not router.allow_migrate(self.connection.alias, self.Migration):
            print(f"Migration not allowed for db: {self.connection.alias}")
            return
        self.ensure_schema()
        self.migration_qs.create(app=app, name=name)
        self.migration_qs.create(app=app, name=name)

    def record_unapplied(self, app, name):
        """Record that a migration was unapplied."""
        if not router.allow_migrate(self.connection.alias, self.Migration):
            return
        self.ensure_schema()
        self.migration_qs.filter(app=app, name=name).delete()
    def flush(self):
        """Delete all migration records. Useful for testing migrations."""
        self.migration_qs.all().delete()
