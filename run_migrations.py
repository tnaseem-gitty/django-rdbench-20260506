import django
from django.core.management import call_command

django.setup()
call_command('migrate')
