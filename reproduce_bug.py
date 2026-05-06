import django
from django.conf import settings
from django.db import models
from django.test import TestCase

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=['__main__'],
)
django.setup()

class JsonFieldHasKeyTest(models.Model):
    data = models.JSONField()

class JsonFieldHasKeyTestCase(TestCase):
    def setUp(self):
        test = JsonFieldHasKeyTest(data={'foo': 'bar'})
        test2 = JsonFieldHasKeyTest(data={'1111': 'bar'})
        test.save()
        test2.save()

    def test_json_field_has_key(self):
        c1 = JsonFieldHasKeyTest.objects.filter(data__has_key='foo').count()
        c2 = JsonFieldHasKeyTest.objects.filter(data__has_key='1111').count()
        print(f"Count for 'foo': {c1}")
        print(f"Count for '1111': {c2}")
        assert c1 == 1, "Should have found 1 entry with key 'foo'"
        assert c2 == 1, "Should have found 1 entry with key '1111'"

if __name__ == '__main__':
    from django.core.management import call_command
    from django.db import connection
    
    # Create the database schema
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(JsonFieldHasKeyTest)
    
    test_case = JsonFieldHasKeyTestCase()
    test_case.setUp()
    test_case.test_json_field_has_key()
    print("Script completed successfully, no errors.")
