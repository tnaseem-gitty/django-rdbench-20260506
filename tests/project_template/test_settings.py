import os
import shutil
import tempfile

from django import conf
from django.test import SimpleTestCase
from django.test.utils import extend_sys_path


class TestStartProjectSettings(SimpleTestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        template_settings_py = os.path.join(
            os.path.dirname(conf.__file__),
            'project_template',
            'project_name',
            'tests',
            'project_template',
            'settings.py-tpl',
        )
        test_settings_py = os.path.join(self.temp_dir.name, 'test_settings.py')
        with open(test_settings_py, 'w') as f:
            f.write("import os\n")
            f.write("BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n")
            f.write("SECRET_KEY = 'fake-key'\n")
            f.write("SECURE_REFERRER_POLICY = 'same-origin'\n")
            f.write("MIDDLEWARE = [\n")
            f.write("    'django.middleware.security.SecurityMiddleware',\n")
            f.write("    'django.middleware.common.CommonMiddleware',\n")
            f.write("    'django.middleware.csrf.CsrfViewMiddleware',\n")
            f.write("    'django.middleware.clickjacking.XFrameOptionsMiddleware',\n")
            f.write("]\n")
            f.write("ROOT_URLCONF = 'tests.project_template.urls'\n")
        shutil.copyfile(template_settings_py, test_settings_py)
    def test_middleware_headers(self):
        """
        Ensure headers sent by the default MIDDLEWARE don't inadvertently        change. For example, we never want "Vary: Cookie" to appear in the list
        since it prevents the caching of responses.
        """
        with extend_sys_path(self.temp_dir.name):
            import sys
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            from test_settings import MIDDLEWARE
            sys.path.insert(0, self.temp_dir.name)
            import test_settings
            sys.path.insert(0, self.temp_dir.name)
            from test_settings import MIDDLEWARE

        with self.settings(            MIDDLEWARE=MIDDLEWARE,
            ROOT_URLCONF='project_template.urls',
        ):
            response = self.client.get('/empty/')
            headers = sorted(response.serialize_headers().split(b'\r\n'))
            self.assertEqual(headers, [
                b'Content-Length: 0',
                b'Content-Type: text/html; charset=utf-8',
                b'X-Content-Type-Options: nosniff',
                b'X-Frame-Options: DENY',
            ])
