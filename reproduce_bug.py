from django.db import models
from django.db.models import F
import datetime

# Set up Django
import django
from django.conf import settings
settings.configure(
    DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
    INSTALLED_APPS=['django.contrib.contenttypes', 'django.contrib.auth'],
    DEFAULT_AUTO_FIELD='django.db.models.AutoField',
)
django.setup()

class Experiment(models.Model):
    estimated_time = models.DurationField()

    class Meta:
        app_label = 'auth'  # Use an existing app label

# Create the table in the database
from django.core.management import call_command
call_command('makemigrations', verbosity=0, interactive=False)
call_command('migrate', verbosity=0, interactive=False)

# Create a sample experiment
Experiment.objects.create(estimated_time=datetime.timedelta(hours=1))

# Try to annotate with a duration expression
delta = datetime.timedelta(days=1)
try:
    list(Experiment.objects.annotate(duration=F('estimated_time') + delta))
    print("Bug not reproduced. The operation succeeded.")
except Exception as e:
    print(f"Bug reproduced. Error: {str(e)}")

print("Script completed.")
