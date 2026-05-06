import os
from django.conf import settings
from django.db.migrations.writer import MigrationWriter
from django.db import migrations, models

# Set up minimal Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'
settings.configure(
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "django.contrib.auth",
    ],
    USE_TZ=True,
)

class TestMigration(migrations.Migration):
    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]

migration = TestMigration('test_app', 'test_migration')
writer = MigrationWriter(migration)
migration_file_contents = writer.as_string()

print("Full migration file contents:")
print(migration_file_contents)

# Extract and print only the imports section
imports_section = migration_file_contents.split('\n\n')[1]  # The imports are in the second block
print("\nImports section:")
print(imports_section)

print("\nScript completed successfully, no errors.")
