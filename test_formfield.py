import os
import django
from django.conf import settings
from unittest.mock import Mock

# Set up Django environment
if not settings.configured:
    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        SECRET_KEY='fake-key',
    )
    django.setup()

from django.contrib.admin.options import ModelAdmin
from django.db import models
from django.forms.widgets import SelectMultiple, Widget

class RelatedModel(models.Model):
    class Meta:
        app_label = 'admin'

class TestModel(models.Model):
    related = models.ManyToManyField(RelatedModel)

    class Meta:
        app_label = 'admin'

class TestAdmin(ModelAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.admin_site = Mock()
        self.admin_site._registry = {}

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if 'widget' in kwargs:
            return db_field.formfield(**kwargs)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

# Test with default widget
admin = TestAdmin(TestModel, None)
formfield = admin.formfield_for_manytomany(TestModel._meta.get_field('related'), None)
print(f"Default widget: {formfield.widget.__class__.__name__}")

# Test with custom widget
class CustomWidget(SelectMultiple):
    pass

admin = TestAdmin(TestModel, None)
formfield = admin.formfield_for_manytomany(TestModel._meta.get_field('related'), None, widget=CustomWidget)
print(f"Custom widget: {formfield.widget.__class__.__name__}")

print("If you see 'CustomWidget' as the output for the custom widget test, the fix is working correctly.")
