from django.core.management import call_command, CommandError
from django.core.management.base import BaseCommand
from django.test import TestCase

class TestCommand(BaseCommand):
    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('--shop-id', type=int)
        group.add_argument('--shop', type=str)

    def handle(self, *args, **options):
        print(f"Received options: {options}")
        if options.get('shop_id') is not None:
            return f"Shop ID: {options['shop_id']}"
        elif options.get('shop'):
            return f"Shop Name: {options['shop']}"
        else:
            return "No valid option provided"

class CallCommandTests(TestCase):
    def test_mutually_exclusive_group(self):
        # Test with shop_id
        result = call_command(TestCommand(), shop_id=1)
        self.assertEqual(result, "Shop ID: 1")

        # Test with shop name
        result = call_command(TestCommand(), shop="Test Shop")
        self.assertEqual(result, "Shop Name: Test Shop")

        # Test with both (should raise an error)
        with self.assertRaises(CommandError):
            call_command(TestCommand(), shop_id=1, shop="Test Shop")

        # Test with neither (should raise an error)
        with self.assertRaises(CommandError):
            call_command(TestCommand())

if __name__ == '__main__':
    import django
    from django.conf import settings
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
    )
    django.setup()
    
    import unittest
    unittest.main()
