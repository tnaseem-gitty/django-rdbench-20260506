import json
from django.test import SimpleTestCase
from django.forms import JSONField

class JSONFieldTest(SimpleTestCase):
    def test_prepare_value_with_unicode(self):
        field = JSONField()
        test_data = {"key": "中国"}
        prepared_value = field.prepare_value(test_data)
        self.assertEqual(json.loads(prepared_value), test_data)
        self.assertIn("中国", prepared_value)

    def test_has_changed_with_unicode(self):
        field = JSONField()
        initial = {"key": "中国"}
        data = json.dumps(initial)
        self.assertFalse(field.has_changed(initial, data))

if __name__ == '__main__':
    import django
    from django.conf import settings
    settings.configure(DEBUG=True)
    django.setup()
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["__main__"])
    exit(bool(failures))
