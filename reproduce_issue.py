import os
import django
from django.conf import settings
from django.core.management import call_command

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_project.settings')

# Initialize Django
django.setup()

# Import the model after Django is set up
from test_project.test_app.models import FooBar

# Run migrations
call_command('migrate')

# Test the model
test_model = FooBar(foo_bar='1')
print(f'FooBar.__str__() returns: {str(test_model)}')
print(f'FooBar.get_foo_bar_display() returns: {test_model.get_foo_bar_display()}')
print(f'FooBar.get_custom_foo_bar_display() returns: {test_model.get_custom_foo_bar_display()}')
print(f'FooBar.custom_display() returns: {test_model.custom_display()}')

print('Script completed successfully, no errors.')
