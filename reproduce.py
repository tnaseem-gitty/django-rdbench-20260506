import django
from django.conf import settings
from django.db import connections
from django.utils import timezone
import datetime

settings.configure(
    USE_TZ=True,
    TIME_ZONE='Europe/Paris',
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
        'legacy': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': 'my.cnf',
            },
            'TIME_ZONE': 'Europe/Paris',
        },
    },
    INSTALLED_APPS=['testapp'],
)
django.setup()
from django.core.management import call_command
call_command('makemigrations', 'testapp')
call_command('migrate', 'testapp')

# Create a timezone-aware datetime object
dt = timezone.make_aware(datetime.datetime(2017, 7, 6, 20, 50))

# Simulate a database query
with connections['default'].cursor() as cursor:
    cursor.execute("SELECT (1) AS `a` FROM `testapp_mymodel` WHERE DATE(my_datetime_field) = '2017-07-06' LIMIT 1;")
    result = cursor.fetchone()
    print(result)

print("Script completed successfully, no errors.")
