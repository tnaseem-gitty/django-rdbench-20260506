import os
import django
from django.db import models, connection
from django.test import TestCase
from django.core.management import call_command
from django.db import connection
from django.test.utils import CaptureQueriesContext

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_test_settings")
django.setup()

# Move OurModel to test_app/models.py
with open('test_app/models.py', 'w') as f:
    f.write('''
from django.db import models

class OurModel(models.Model):
    our_field = models.JSONField()
''')

from test_app.models import OurModel

class JSONFieldInLookupTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        OurModel.objects.create(our_field={"key": 0})
        OurModel.objects.create(our_field={"key": 1})
        OurModel.objects.create(our_field={"key": 2})

    def test_in_lookup(self):
        with CaptureQueriesContext(connection) as queries:
            first_filter = {'our_field__key__in': [0]}
            first_items = list(OurModel.objects.filter(**first_filter))
            print(f"Items with __in lookup: {len(first_items)}")
            print(f"SQL for __in lookup: {queries[-1]['sql']}")

        with CaptureQueriesContext(connection) as queries:
            second_filter = {'our_field__key': 0}
            second_items = list(OurModel.objects.filter(**second_filter))
            print(f"Items with direct lookup: {len(second_items)}")
            print(f"SQL for direct lookup: {queries[-1]['sql']}")

        self.assertEqual(len(first_items), len(second_items), "The __in lookup is not working as expected")

        with CaptureQueriesContext(connection) as queries:
            third_filter = {'our_field__key__in': [0, 1]}
            third_items = list(OurModel.objects.filter(**third_filter))
            print(f"Items with multiple values __in lookup: {len(third_items)}")
            print(f"SQL for multiple values __in lookup: {queries[-1]['sql']}")

        self.assertEqual(len(third_items), 2, "The __in lookup with multiple values is not working as expected")

if __name__ == '__main__':
    # Make migrations for test_app
    call_command('makemigrations', 'test_app')
    
    # Apply all migrations
    call_command('migrate')
    
    print("Running the test...")
    test = JSONFieldInLookupTest()
    test.setUpTestData()
    test.test_in_lookup()
    print("Test completed.")
            kwargs['encoder'] = self.encoder
        if self.decoder is not None:
            kwargs['decoder'] = self.decoder
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        if connection.features.has_native_json_field and self.decoder is None:
            return value
        try:
            return json.loads(value, cls=self.decoder)
        except json.JSONDecodeError:
            return value

    def get_internal_type(self):
        return 'JSONField'

    def get_prep_value(self, value):
        if value is None:
            return value
        return json.dumps(value, cls=self.encoder)

    def get_transform(self, name):
        transform = super().get_transform(name)
        if transform:
            return transform
        return KeyTransformFactory(name)

    def select_format(self, compiler, sql, params):
        if (
            compiler.connection.features.has_native_json_field and
            self.decoder is not None
        ):
            return compiler.connection.ops.json_cast_text_sql(sql), params
        return sql, params

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        try:
            json.dumps(value, cls=self.encoder)
        except TypeError:
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def value_to_string(self, obj):
        return self.value_from_object(obj)

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.JSONField,
            'encoder': self.encoder,
            'decoder': self.decoder,
            **kwargs,
        })


class KeyTransform(Transform):
    def __init__(self, key_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_name = key_name

    def as_sql(self, compiler, connection):
        key_transforms = [self.key_name]
        previous = self.lhs
        while isinstance(previous, KeyTransform):
            key_transforms.insert(0, previous.key_name)
            previous = previous.lhs
        lhs, params = compiler.compile(previous)
        for key in key_transforms:
            lhs = "(%s %s %%s)" % (
                lhs,
                connection.ops.json_key_extract_op,
            )
            params.append(key)
        return lhs, params

    def preprocess_lhs(self, compiler, connection, lhs_only=False):
        if not lhs_only:
            key_transforms = [self.key_name]
            previous = self.lhs
            while isinstance(previous, KeyTransform):
                key_transforms.insert(0, previous.key_name)
                previous = previous.lhs
            return previous, key_transforms
        return super().preprocess_lhs(compiler, connection, lhs_only)


class KeyTransformFactory:

    def __init__(self, key_name):
        self.key_name = key_name

    def __call__(self, *args, **kwargs):
        return KeyTransform(self.key_name, *args, **kwargs)


class KeyTextTransform(KeyTransform):
    operator = '->>'
    output_field = Field()

    def __init__(self, key_name, *args, **kwargs):
        super().__init__(key_name, *args, **kwargs)


class KeyTransformTextLookupMixin:
    """
    Mixin for combining with a lookup expecting a text lhs from a JSONField
    key lookup. Make use of the ->> operator instead of casting key values to
    text and performing the lookup on the resulting representation.
    """
    def __init__(self, key_transform, *args, **kwargs):
        assert isinstance(key_transform, KeyTransform)
        key_text_transform = KeyTextTransform(
            key_transform.key_name, *key_transform.source_expressions,
            **key_transform.extra,
        )
        super().__init__(key_text_transform, *args, **kwargs)


@JSONField.register_lookup
class KeyTransformIExact(KeyTransformTextLookupMixin, lookups.IExact):
    pass


@JSONField.register_lookup
class KeyTransformIContains(KeyTransformTextLookupMixin, lookups.IContains):
    pass


@JSONField.register_lookup
class KeyTransformStartsWith(KeyTransformTextLookupMixin, lookups.StartsWith):
    pass


@JSONField.register_lookup
class KeyTransformIStartsWith(KeyTransformTextLookupMixin, lookups.IStartsWith):
    pass


@JSONField.register_lookup
class KeyTransformEndsWith(KeyTransformTextLookupMixin, lookups.EndsWith):
    pass


@JSONField.register_lookup
class KeyTransformIEndsWith(KeyTransformTextLookupMixin, lookups.IEndsWith):
    pass


@JSONField.register_lookup
class KeyTransformRegex(KeyTransformTextLookupMixin, lookups.Regex):
    pass


@JSONField.register_lookup
class KeyTransformIRegex(KeyTransformTextLookupMixin, lookups.IRegex):
    pass


class KeyTransformNumericLookupMixin:
    def process_rhs(self, compiler, connection):
        rhs, rhs_params = super().process_rhs(compiler, connection)
        if not connection.features.has_native_json_field:
            rhs_params = [json.loads(value) for value in rhs_params]
        return rhs, rhs_params

class KeyTransformLt(KeyTransformNumericLookupMixin, lookups.LessThan):
    pass


class KeyTransformLte(KeyTransformNumericLookupMixin, lookups.LessThanOrEqual):
    pass


class KeyTransformGt(KeyTransformNumericLookupMixin, lookups.GreaterThan):
    pass


class KeyTransformGte(KeyTransformNumericLookupMixin, lookups.GreaterThanOrEqual):
    pass


class KeyTransformIn(KeyTransformTextLookupMixin, lookups.In):
    def as_sql(self, compiler, connection):
        # Get the SQL for the key transform
        lhs, lhs_params = self.process_lhs(compiler, connection)
        # Get the SQL for the IN values
        rhs, rhs_params = self.process_rhs(compiler, connection)
        # Combine them
        params = lhs_params + list(rhs_params)
        return '%s IN %s' % (lhs, rhs), params

KeyTransform.register_lookup(KeyTransformIn)
