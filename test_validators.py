from django.core.validators import RegexValidator, URLValidator, validate_email, validate_ipv4_address, validate_ipv6_address
from django.core.exceptions import ValidationError
import unittest

class TestValidators(unittest.TestCase):
    def test_regex_validator(self):
        validator = RegexValidator(regex=r'^[0-9]+$', message='Enter a valid number.')
        with self.assertRaisesRegex(ValidationError, r"\['Enter a valid number.'\]"):
            validator('abc')

    def test_url_validator(self):
        validator = URLValidator()
        with self.assertRaisesRegex(ValidationError, r'\[\'Enter a valid URL. "%(value)s" is not a valid URL.\'\]'):
            validator('invalid-url')

    def test_email_validator(self):
        with self.assertRaisesRegex(ValidationError, r'Enter a valid email address.'):
            validate_email('invalid-email')

    def test_ipv4_validator(self):
        with self.assertRaisesRegex(ValidationError, r'Enter a valid IPv4 address. "256.0.0.1" is not a valid IPv4 address.'):
            validate_ipv4_address('256.0.0.1')

    def test_ipv6_validator(self):
        with self.assertRaisesRegex(ValidationError, r'Enter a valid IPv6 address. "2001:db8::g" is not a valid IPv6 address.'):
            validate_ipv6_address('2001:db8::g')

if __name__ == '__main__':
    unittest.main()
