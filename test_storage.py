import os
import django
import unittest
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
        INSTALLED_APPS=[
            'django.contrib.staticfiles',
        ],
        STATIC_URL='/static/',
        STATIC_ROOT=os.path.join(os.path.dirname(__file__), 'test_static_root'),
    )
    django.setup()

class TestManifestStaticFilesStorage(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.temp_dir = os.path.join(os.path.dirname(__file__), 'test_static_root')
        if not os.path.exists(cls.temp_dir):
            os.makedirs(cls.temp_dir)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if os.path.exists(cls.temp_dir):
            for root, dirs, files in os.walk(cls.temp_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(cls.temp_dir)

    @override_settings(STATIC_ROOT=os.path.join(os.path.dirname(__file__), 'test_static_root'))
    def test_max_post_process_passes_zero(self):
        class CustomManifestStaticFilesStorage(ManifestStaticFilesStorage):
            max_post_process_passes = 0

        storage = CustomManifestStaticFilesStorage()
        
        # Create a dummy file
        file_content = b"This is a test file"
        file_name = "test.txt"
        full_path = os.path.join(self.temp_dir, file_name)
        with open(full_path, 'wb') as f:
            f.write(file_content)

        # Run post_process
        try:
            list(storage.post_process({'test.txt': (FileSystemStorage(), full_path)}))
        except UnboundLocalError:
            self.fail("UnboundLocalError was raised")

        print("Test completed successfully.")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestManifestStaticFilesStorage)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.failures or result.errors:
        exit(1)
