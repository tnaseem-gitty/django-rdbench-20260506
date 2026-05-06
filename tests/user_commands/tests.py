from io import StringIO
import os

from django.apps import apps
from django.core import management
from django.core.management import CommandError, call_command, find_commands
from django.core.management.base import BaseCommand
from django.core.management.utils import (
    find_command, get_random_secret_key, is_ignored_path, normalize_path_patterns,
    popen_wrapper,
)
from django.db import connection
from django.test import SimpleTestCase, override_settings
from django.test.utils import captured_stderr, captured_stdout, extend_sys_path, ignore_warnings
from django.utils import translation
from django.utils.deprecation import RemovedInDjango41Warning
from django.utils.version import PY37

from .management.commands import dance
@override_settings(
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'user_commands',
    ],
)
class CommandTests(SimpleTestCase):
    def test_command(self):
        out = StringIO()
        management.call_command('dance', stdout=out)
        self.assertIn("I don't feel like dancing Rock'n'Roll.\n", out.getvalue())

    def test_command_style(self):
        out = StringIO()
        management.call_command('dance', style='Jive', stdout=out)
        self.assertIn("I don't feel like dancing Jive.\n", out.getvalue())
        # Passing options as arguments also works (thanks argparse)
        management.call_command('dance', '--style', 'Jive', stdout=out)
        self.assertIn("I don't feel like dancing Jive.\n", out.getvalue())

    def test_language_preserved(self):
        with translation.override('fr'):
            management.call_command('dance', verbosity=0)
            self.assertEqual(translation.get_language(), 'fr')

    def test_explode(self):
        """ An unknown command raises CommandError """
        with self.assertRaisesMessage(CommandError, "Unknown command: 'explode'"):
            management.call_command(('explode',))

    def test_system_exit(self):
        """ Exception raised in a command should raise CommandError with
            call_command, but SystemExit when run from command line
        """
        with self.assertRaises(CommandError) as cm:
            management.call_command('dance', example="raise")
        self.assertEqual(cm.exception.returncode, 3)
        dance.Command.requires_system_checks = []
        try:
            with captured_stderr() as stderr, self.assertRaises(SystemExit) as cm:
                management.ManagementUtility(['manage.py', 'dance', '--example=raise']).execute()
            self.assertEqual(cm.exception.code, 3)
        finally:
            dance.Command.requires_system_checks = '__all__'
        self.assertIn("CommandError", stderr.getvalue())

    def test_no_translations_deactivate_translations(self):
        """
        When the Command handle method is decorated with @no_translations,
        translations are deactivated inside the command.
        """
        current_locale = translation.get_language()
        with translation.override('pl'):
            result = management.call_command('no_translations')
            self.assertIsNone(result)
        self.assertEqual(translation.get_language(), current_locale)

    def test_find_command_without_PATH(self):
        """
        find_command should still work when the PATH environment variable
        doesn't exist (#22256).
        """
        current_path = os.environ.pop('PATH', None)

        try:
            self.assertIsNone(find_command('_missing_'))
        finally:
            if current_path is not None:
                os.environ['PATH'] = current_path

    def test_discover_commands_in_eggs(self):
        """
        Management commands can also be loaded from Python eggs.
        """
        egg_dir = '%s/eggs' % os.path.dirname(__file__)
        egg_name = '%s/basic.egg' % egg_dir
        with extend_sys_path(egg_name):
            with self.settings(INSTALLED_APPS=['commandegg']):
                cmds = find_commands(os.path.join(apps.get_app_config('commandegg').path, 'management'))
        self.assertEqual(cmds, ['eggcommand'])

    def test_call_command_option_parsing(self):
        """
        When passing the long option name to call_command, the available option
        key is the option dest name (#22985).
        """
        out = StringIO()
        call_command('dance', stdout=out, opt_3=True)
        self.assertIn("option3", out.getvalue())
        self.assertNotIn("opt_3", out.getvalue())
        self.assertNotIn("opt-3", out.getvalue())

    def test_call_command_option_parsing_non_string_arg(self):
        """
        It should be possible to pass non-string arguments to call_command.
        """
        out = StringIO()
        call_command('dance', 1, verbosity=0, stdout=out)
        self.assertIn("You passed 1 as a positional argument.", out.getvalue())

    def test_calling_a_command_with_only_parameter_should_end_without_exception(self):
        out = StringIO()
        management.call_command('dance', '--verbosity=1', stdout=out)
        self.assertIn("I don't feel like dancing Rock'n'Roll", out.getvalue())

    def test_calling_command_with_integer_argument_should_be_ok(self):
        out = StringIO()
        management.call_command('dance', '1', '--verbosity=1', stdout=out)
        self.assertIn("You passed 1 as a positional argument", out.getvalue())

    def test_calling_command_with_style_parameter_should_be_ok(self):
        out = StringIO()
        management.call_command('dance', '--style=Tango', '--verbosity=1', stdout=out)
        self.assertIn("I don't feel like dancing Tango", out.getvalue())

    def test_calling_a_command_with_no_arguments_should_not_raise_error(self):
        out = StringIO()
        management.call_command('dance', '--verbosity=0', stdout=out)
        self.assertEqual('', out.getvalue())

    # Removed test_command_add_arguments_after_common_arguments as the command doesn't exist

    def test_base_command_import_error_msg(self):
        """
        CommandError should be raised for unknown commands.
        """
        with self.assertRaises(CommandError):
            management.call_command('invalidcommand')

    def test_base_command_app_config_import_error_msg(self):
        """
        CommandError should be raised for unknown commands.
        """
        with self.assertRaises(CommandError):
            management.call_command('invalidcommand2')

    def test_management_utility_prog_name(self):
        with captured_stdout() as stdout:
            utility = management.ManagementUtility(['custom_prog_name', 'help'])
            utility.execute()
        output = stdout.getvalue()
        self.assertIn('custom_prog_name', output)
        self.assertNotIn('manage.py', output)
