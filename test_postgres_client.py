import unittest
from unittest.mock import patch, MagicMock
from django.db.backends.postgresql import client

class TestPostgresClient(unittest.TestCase):
    @patch('django.db.backends.postgresql.client.subprocess')
    @patch('django.db.backends.postgresql.client.os')
    @patch('django.db.backends.postgresql.client.signal')
    def test_runshell_db(self, mock_signal, mock_os, mock_subprocess):
        # Mock the necessary objects and methods
        connection = MagicMock()
        connection.get_connection_params.return_value = {
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_password',
            'host': 'localhost',
            'port': '5432'
        }

        # Mock os.environ.copy()
        mock_env = {}
        mock_os.environ.copy.return_value = mock_env
        mock_os.environ.copy.side_effect = lambda: print("os.environ.copy() called") or mock_env

        # Call the method we're testing
        conn_params = connection.get_connection_params.return_value
        print("conn_params:", conn_params)
        print("Before runshell_db")
        client.DatabaseClient(connection).runshell_db(conn_params)
        print("After runshell_db")
        print("Final mock_env:", mock_env)

        # Assert that subprocess.run was called with the correct arguments
        mock_subprocess.run.assert_called_once()
        args, kwargs = mock_subprocess.run.call_args

        # Debug print statements
        print("subprocess.run args:", args)
        print("subprocess.run kwargs:", kwargs)
        print("mock_os.environ.copy() called:", mock_os.environ.copy.called)
        print("mock_os.environ.copy() call count:", mock_os.environ.copy.call_count)
        print("mock_os.environ.copy() return value:", mock_os.environ.copy.return_value)
        self.assertEqual(args[0][0], 'psql')
        self.assertIn('test_db', args[0])
        self.assertIn('test_user', args[0])
        self.assertIn('localhost', args[0])
        self.assertIn('5432', args[0])

        # Check that PGPASSWORD is set in the environment passed to subprocess.run
        self.assertIn('PGPASSWORD', kwargs['env'])
        self.assertEqual(kwargs['env']['PGPASSWORD'], 'test_password')

        # Check that check=True is set
        self.assertTrue(kwargs['check'])

        # Check that PGPASSWORD is removed from the environment after the subprocess call
        self.assertNotIn('PGPASSWORD', mock_env)

if __name__ == '__main__':
    unittest.main()
