from django.db import models
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

class TestMultipleOneToOneFields(TestCase):
    def test_multiple_onetoone_fields(self):
        class Document(models.Model):
            pass

        # This should not raise ImproperlyConfigured
        class Picking(Document):
            document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')
            origin = models.OneToOneField(Document, related_name='picking', on_delete=models.PROTECT)

        # This should also not raise ImproperlyConfigured
        class AnotherPicking(Document):
            origin = models.OneToOneField(Document, related_name='another_picking', on_delete=models.PROTECT)
            document_ptr = models.OneToOneField(Document, on_delete=models.CASCADE, parent_link=True, related_name='+')

        self.assertTrue(issubclass(Picking, Document))
        self.assertTrue(issubclass(AnotherPicking, Document))

        # Ensure that the parent_link is correctly identified
        self.assertEqual(Picking._meta.parents[Document], Picking._meta.get_field('document_ptr'))
        self.assertEqual(AnotherPicking._meta.parents[Document], AnotherPicking._meta.get_field('document_ptr'))

        # Ensure that the non-parent_link OneToOneField is not treated as a parent link
        self.assertNotIn(Document, Picking._meta.get_field('origin').related_model._meta.parents)
        self.assertNotIn(Document, AnotherPicking._meta.get_field('origin').related_model._meta.parents)

