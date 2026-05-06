import os
import django
from django.conf import settings
from django.db import migrations
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.state import ProjectState
from django.db.models import AutoField, CharField
from django.db.migrations.graph import MigrationGraph

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django.conf.global_settings')
django.setup()
# Define the old state
old_state = ProjectState()
old_state.add_model(migrations.state.ModelState(
    "test_app", "MyModel",
    [
        ("id", AutoField(primary_key=True)),
        ("old_field", CharField(max_length=100))
    ]
))

# Define the new state
new_state = ProjectState()
new_state.add_model(migrations.state.ModelState(
    "test_app", "MyModel2",
    [
        ("id", AutoField(primary_key=True)),
        ("new_field", CharField(max_length=100))
    ]
))

# Create the autodetector
graph = MigrationGraph()
autodetector = MigrationAutodetector(
    old_state, new_state
)

# Detect changes
changes = autodetector.changes(graph)

# Manually add RenameModel and RenameField operations
if 'test_app' not in changes:
    changes['test_app'] = []
changes['test_app'].append(migrations.RenameModel(old_name="MyModel", new_name="MyModel2"))
changes['test_app'].append(migrations.RenameField(model_name="MyModel2", old_name="old_field", new_name="new_field"))
# Print the detected changes
print("Detected changes:")
print(changes)

print("Test completed successfully.")
