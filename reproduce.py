import django
from django.conf import settings

settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ]
)

django.setup()

from django.db import models

class MyField(models.TextField):
    pass

class MyBaseModel(models.Model):
    class Meta:
        abstract = True

class MyMixin:
    pass

class MyModel(MyMixin, MyBaseModel):
    class Meta:
        app_label = 'app'

import __main__ as app
# import app.models
from django.db import migrations

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('name', MyField(primary_key=True, serialize=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(MyMixin, models.Model),
        ),
    ]

# Attempt to instantiate the Migration class to replicate the error
try:
    migration = Migration('test_migration', 'app')
    print("Migration created successfully.")
except NameError as e:
    print(f"Error: {e}")

