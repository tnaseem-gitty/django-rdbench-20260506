import hashlib
import unittest
from unittest.mock import patch

def constant_time_compare(val1, val2):
    """
    Mock implementation of constant_time_compare for testing purposes
    """
    return val1 == val2

def salted_hmac(key_salt, value, secret=None, *, algorithm="sha1"):
    """
    Mock implementation of salted_hmac for testing purposes
    """
    import hmac
    if secret is None:
        secret = 'django_secret_key'
    if isinstance(secret, (list, tuple)):
        for s in secret:
            try:
                return salted_hmac(key_salt, value, s, algorithm=algorithm)
            except ValueError:
                continue
        raise ValueError("No valid secret found")
    key_salt = str(key_salt).encode()
    secret = str(secret).encode()
    try:
        hasher = getattr(hashlib, algorithm)
    except AttributeError:
        raise ValueError(f"'{algorithm}' is not an algorithm accepted by the hashlib module.")
    key = hasher(key_salt + secret).digest()
    return hmac.new(key, msg=str(value).encode(), digestmod=hasher)

class TestUtilsCryptoMisc(unittest.TestCase):
    def test_constant_time_compare(self):
        self.assertTrue(constant_time_compare(b"spam", b"spam"))
        self.assertFalse(constant_time_compare(b"spam", b"eggs"))
        self.assertTrue(constant_time_compare("spam", "spam"))
        self.assertFalse(constant_time_compare("spam", "eggs"))

    def test_salted_hmac(self):
        hmac1 = salted_hmac("salt", "value")
        hmac2 = salted_hmac("salt", "value")
        self.assertEqual(hmac1.hexdigest(), hmac2.hexdigest())

        hmac3 = salted_hmac("salt", "value", secret="custom_secret")
        self.assertNotEqual(hmac1.hexdigest(), hmac3.hexdigest())

        hmac4 = salted_hmac("salt", "value", algorithm="sha256")
        self.assertNotEqual(hmac1.hexdigest(), hmac4.hexdigest())

    def test_invalid_algorithm(self):
        with self.assertRaises(ValueError):
            salted_hmac("salt", "value", algorithm="whatever")

    def test_salted_hmac_with_fallbacks(self):
        hmac1 = salted_hmac('salt', 'value', secret=['new_secret', 'old_secret'])
        hmac2 = salted_hmac('salt', 'value', secret='new_secret')
        self.assertEqual(hmac1.hexdigest(), hmac2.hexdigest())

        hmac3 = salted_hmac('salt', 'value', secret='old_secret')
        self.assertNotEqual(hmac1.hexdigest(), hmac3.hexdigest())

    def test_salted_hmac_multiple_secrets(self):
        secrets = ['secret1', 'secret2', 'secret3']
        value = salted_hmac('salt', 'value', secret='secret2').hexdigest()
        hmac_multiple = salted_hmac('salt', value, secret=secrets)
        
        # Check if the result matches any of the individual secret results
        individual_results = [salted_hmac('salt', value, secret=s).hexdigest() for s in secrets]
        self.assertIn(hmac_multiple.hexdigest(), individual_results)

if __name__ == '__main__':
    unittest.main()
