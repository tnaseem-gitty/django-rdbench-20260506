import os
import django
from django.db.migrations.executor import MigrationExecutor
from django.db import connection

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reproduce_settings')
django.setup()

# Simulate unapplying a squashed migration
executor = MigrationExecutor(connection)
executor.migrate([('test_migrations_squashed_extra', '0001_squashed_0002')])

# Check if the squashed migration is marked as unapplied
applied_migrations = executor.loader.applied_migrations
print('Squashed migration unapplied:', ('test_migrations_squashed_extra', '0001_squashed_0002') not in applied_migrations)
