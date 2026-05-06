from django.db import models

class TestModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.CharField(max_length=100)

    class Meta:
        unique_together = (('field1', 'field2'),)
        index_together = (('field1', 'field2'),)
