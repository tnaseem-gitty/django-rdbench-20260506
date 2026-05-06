import django
from django.conf import settings
from django.db import models
from django.core.management import call_command

# Configure settings for the Django project
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'test_one',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
)

# Initialize Django
django.setup()

# Define the initial model
class MyModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'test_one'

# Create the initial migration
call_command('makemigrations', 'test_one')
call_command('makemigrations', 'test_one', '--empty', '--name', 'rename_model_and_field')
with open('test_one/migrations/0002_rename_model_and_field.py', 'w') as f:
    f.write('''
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('test_one', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MyModel',
            new_name='MyModel2',
        ),
        migrations.RenameField(
            model_name='mymodel2',
            old_name='name',
            new_name='new_name',
        ),
    ]
''')
call_command('makemigrations', 'test_one', '--empty', '--name', 'merge_migrations')
with open('test_one/migrations/0003_merge_migrations.py', 'w') as f:
    f.write('''
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('test_one', '0002_rename_model_and_field'),
        ('test_one', '0001_initial'),
    ]

    operations = [
    ]
''')
call_command('makemigrations', '--merge')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
call_command('migrate', 'test_one')
