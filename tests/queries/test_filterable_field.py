from django.test import TestCase
from django.db import models
from django.core.exceptions import FieldError

class ProductMetaDataType(models.Model):
    label = models.CharField(max_length=255, unique=True)
    filterable = models.BooleanField(default=False)

class ProductMetaData(models.Model):
    value = models.TextField()
    metadata_type = models.ForeignKey(ProductMetaDataType, on_delete=models.CASCADE)

class FilterableFieldTest(TestCase):
    def test_filter_on_non_filterable_field(self):
        brand_metadata = ProductMetaDataType.objects.create(label='Brand', filterable=False)
        ProductMetaData.objects.create(value='Dark Vador', metadata_type=brand_metadata)

        # This should not raise an exception
        result = ProductMetaData.objects.filter(value='Dark Vador', metadata_type=brand_metadata)
        self.assertEqual(result.count(), 1)
