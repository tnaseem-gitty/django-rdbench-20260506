print("Starting test_loader.py")

from django.conf import settings

settings.configure(
    INSTALLED_APPS=[
        'mock_app',
    ],
)

import sys
import types
from django.apps import AppConfig, apps
from django.db.migrations.loader import MigrationLoader
from importlib import import_module

# Create a mock module without __file__ but with __path__ as a list
mock_module = types.ModuleType("mock_module")
mock_module.__path__ = ["mock_path"]

# Add the mock module to sys.modules
sys.modules["mock_app"] = mock_module

# Create a mock AppConfig
class MockAppConfig(AppConfig):
    name = "mock_app"
    label = "mock_app"

# Add the mock AppConfig to apps
apps.populate(settings.INSTALLED_APPS)

# Create a MigrationLoader instance and call load_disk
loader = MigrationLoader(connection=None, load=False)
loader.load_disk()

# Check if the mock app is in unmigrated_apps
print(f"unmigrated_apps: {loader.unmigrated_apps}")
assert "mock_app" not in loader.unmigrated_apps, "Mock app should not be in unmigrated_apps"

print("Test completed successfully, no errors.")

print("Test completed successfully, no errors.")
