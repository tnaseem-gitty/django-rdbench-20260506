from django.core.management import call_command

# Simulate the dbshell command with additional parameters
call_command('dbshell', '--', '-c', 'SELECT 1;')
