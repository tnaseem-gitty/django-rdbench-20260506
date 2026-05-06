from django.contrib.admin import ModelAdmin, VERTICAL
from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.db import models

class EmptyLabelModel(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

class EmptyLabelModelAdmin(ModelAdmin):
    radio_fields = {'parent': VERTICAL}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs['empty_label'] = "Custom Empty Label"
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class EmptyLabelTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_empty_label_default(self):
        ma = ModelAdmin(EmptyLabelModel, self.site)
        form_field = ma.formfield_for_foreignkey(EmptyLabelModel._meta.get_field('parent'), None)
        self.assertEqual(form_field.empty_label, "---------")

    def test_empty_label_custom(self):
        ma = EmptyLabelModelAdmin(EmptyLabelModel, self.site)
        form_field = ma.formfield_for_foreignkey(EmptyLabelModel._meta.get_field('parent'), None)
        self.assertEqual(form_field.empty_label, "Custom Empty Label")

print("Test file created successfully.")
