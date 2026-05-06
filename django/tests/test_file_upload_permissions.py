import os
import tempfile
from django.core.files.storage import FileSystemStorage
from django.test import TestCase

class FileUploadPermissionsTest(TestCase):
    def test_default_file_upload_permissions(self):
        storage = FileSystemStorage()
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b'Test content')
            temp_file.flush()
            temp_file_name = temp_file.name

        # Save the file using FileSystemStorage
        saved_file_name = storage.save('test_file.txt', open(temp_file_name, 'rb'))

        # Get the file path
        file_path = storage.path(saved_file_name)

        # Check the file permissions
        file_permissions = oct(os.stat(file_path).st_mode & 0o777)
        self.assertEqual(file_permissions, '0o644')

        # Clean up
        os.remove(file_path)
        os.remove(temp_file_name)
