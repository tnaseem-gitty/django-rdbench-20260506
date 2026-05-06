from django.core.management import call_command
from django.test import TestCase
from unittest.mock import patch

class DbShellCommandTest(TestCase):
    @patch('django.db.backends.postgresql.client.DatabaseClient.runshell')
    def test_dbshell_command(self, mock_runshell):
        call_command('dbshell', '--', '-c', 'SELECT 1;')
        mock_runshell.assert_called_once_with(['--', '-c', 'SELECT 1;'])
