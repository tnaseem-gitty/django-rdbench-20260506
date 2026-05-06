import os
import django
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import models

# Minimal settings configuration
settings.configure(
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        '__main__',  # This allows the models in this script to be recognized
    ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
        }
)

django.setup()

class CustomModel(models.Model):
    name = models.CharField(max_length=16)

class ProxyCustomModel(CustomModel):
    class Meta:
        proxy = True

class AnotherModel(models.Model):
    custom = models.ForeignKey(
        ProxyCustomModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Create the tables
        call_command('makemigrations', '__main__')
        call_command('migrate')
        list(AnotherModel.objects.select_related("custom").only("custom__name").all())

if __name__ == "__main__":
    command = Command()
    command.handle()
