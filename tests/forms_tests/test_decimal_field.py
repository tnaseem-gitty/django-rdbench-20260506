from decimal import Decimal
from django.core.exceptions import ValidationError
from django.forms import DecimalField
from django.test import SimpleTestCase

class DecimalFieldTest(SimpleTestCase):
    def test_decimalfield_1(self):
        f = DecimalField()
        with self.assertRaises(ValidationError) as cm:
            f.clean({'key': 'value'})
        self.assertEqual(cm.exception.messages, ['Enter a number.'])

    def test_decimalfield_2(self):
        f = DecimalField()
        self.assertEqual(f.clean('3.14'), Decimal('3.14'))

    def test_decimalfield_3(self):
        f = DecimalField()
        with self.assertRaises(ValidationError) as cm:
            f.clean('foo')
        self.assertEqual(cm.exception.messages, ['Enter a number.'])
