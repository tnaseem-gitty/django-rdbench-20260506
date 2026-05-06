import django
from django.conf import settings
from django.db import models
from django.db.models import FilteredRelation, Q, F, Case, When

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
        '__main__',
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    SECRET_KEY='dummy-secret-key'
)

django.setup()

class MyNestedModel(models.Model):
    zone = models.CharField(max_length=100)
    is_all = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = '__main__'

class MyModel(models.Model):
    zone = models.CharField(max_length=100)
    myrelation = models.ForeignKey(MyNestedModel, on_delete=models.CASCADE, related_name='nested')

    class Meta:
        app_label = '__main__'

qs = MyModel.objects.alias(
    relation_zone=FilteredRelation(
        "myrelation__nested",
        condition=Q(myrelation__nested__zone=F("zone"))
    )
).annotate(
    price_zone=F("relation_zone__price")
)

print(str(qs.query))
