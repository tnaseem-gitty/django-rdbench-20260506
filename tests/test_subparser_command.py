from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase
from io import StringIO
import sys

class TestSubparserCommand(SimpleTestCase):
    def test_subparser_command(self):
        # Test successful execution
        out = StringIO()
        sys.stdout = out
        call_command('test_subparser', 'create', 'test_object')
        self.assertIn('Creating object with name: test_object', out.getvalue())

        # Test missing subcommand
        with self.assertRaises(CommandError) as cm:
            call_command('test_subparser')
        self.assertIn('the following arguments are required: subcommand', str(cm.exception))

        # Test missing argument for subcommand
        with self.assertRaises(CommandError) as cm:
            call_command('test_subparser', 'create')
        self.assertIn('the following arguments are required: name', str(cm.exception))

        # Reset stdout
        sys.stdout = sys.__stdout__

