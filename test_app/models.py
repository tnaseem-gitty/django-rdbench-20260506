import django
from django.conf import settings
from django.db import models
from django.db.models.functions import ExtractIsoYear

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'test_app',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)

django.setup()

from test_app.models import DTModel

# annotation works
qs = DTModel.objects.annotate(extracted=ExtractIsoYear('start_date')).only('id')
print(qs.query)

# explicit annotation used in filter does not use "extracted" and adds BETWEEN
print(qs.filter(extracted=2020).query)

# implicit lookup uses BETWEEN
print(DTModel.objects.filter(start_date__iso_year=2020).only('id').query)
