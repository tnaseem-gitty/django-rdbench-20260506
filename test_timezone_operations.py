import unittest
from unittest.mock import Mock

class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        self.ops = Mock()
        self.ops._prepare_tzname_delta = lambda tzname: (
            '+' + tzname.split('GMT', 1)[1][1:] if tzname.startswith('Etc/GMT-') else
            '-' + tzname.split('GMT', 1)[1][1:] if tzname.startswith('Etc/GMT+') else
            tzname.replace('+', '-') if '+' in tzname else
            tzname.replace('-', '+') if '-' in tzname else
            tzname
        )

    def test_prepare_tzname_delta(self):
        self.assertEqual(self.ops._prepare_tzname_delta('Etc/GMT-10'), '+10')
        self.assertEqual(self.ops._prepare_tzname_delta('Etc/GMT+10'), '-10')
        self.assertEqual(self.ops._prepare_tzname_delta('UTC+10'), 'UTC-10')
        self.assertEqual(self.ops._prepare_tzname_delta('UTC-10'), 'UTC+10')
        self.assertEqual(self.ops._prepare_tzname_delta('America/New_York'), 'America/New_York')

if __name__ == '__main__':
    unittest.main()
