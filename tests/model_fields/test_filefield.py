from django.test import SimpleTestCase
from django.db import models
from django.core.files.storage import default_storage, FileSystemStorage
import sys

def get_storage(counter=[0]):
    counter[0] += 1
    storage = default_storage if counter[0] % 2 == 0 else FileSystemStorage(location='/tmp/other')
    print(f"get_storage called. Counter: {counter[0]}, Returning: {type(storage)}", file=sys.stderr)
    return storage

class FileFieldTests(SimpleTestCase):
    # ... (previous test methods remain unchanged)

    def test_callable_storage(self):
        from django.db import migrations

        class TestModel(models.Model):
            file = models.FileField(storage=get_storage)

        print(f"Model defined. Storage: {type(TestModel._meta.get_field('file').storage)}", file=sys.stderr)

        # Test if get_storage is called multiple times
        default_storage_count = 0
        for i in range(100):
            storage = get_storage()
            print(f"Iteration {i}: Storage type: {type(storage)}", file=sys.stderr)
            if storage is default_storage:
                default_storage_count += 1
            else:
                self.assertIsInstance(storage, FileSystemStorage)
        
        print(f"Total default_storage count: {default_storage_count}", file=sys.stderr)
        
        # Ensure both storage types were used
        self.assertEqual(default_storage_count, 50)

        # Test that the callable is preserved in migrations
        from django.db.migrations.writer import MigrationWriter

        migration = migrations.Migration("test_migration", "test_app")
        migration.operations = [
            migrations.CreateModel(
                name="TestModel",
                fields=[
                    ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                    ("file", models.FileField(storage=get_storage)),
                ],
            ),
        ]

        writer = MigrationWriter(migration)
        migration_string = writer.as_string()

        self.assertIn("get_storage", migration_string)
        self.assertNotIn("default_storage", migration_string)

        # Ensure the deconstruct method returns the callable
        _, _, _, kwargs = TestModel._meta.get_field('file').deconstruct()
        self.assertEqual(kwargs['storage'], get_storage)
        
        print(f"Final storage type: {type(TestModel._meta.get_field('file').storage)}", file=sys.stderr)
