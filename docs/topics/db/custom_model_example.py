"""
Example of how to handle saving objects with existing primary keys.

This example demonstrates how to modify the save() method of a model
to update existing objects when saving with an existing primary key,
instead of raising an IntegrityError.
"""

from django.db import models
import uuid

class Sample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(blank=True, max_length=100)

    def save(self, *args, **kwargs):
        try:
            existing = Sample.objects.get(pk=self.pk)
            for field in self._meta.fields:
                if field.name != 'id':
                    setattr(existing, field.name, getattr(self, field.name))
            super(Sample, existing).save(*args, **kwargs)
        except Sample.DoesNotExist:
            super().save(*args, **kwargs)

"""
Usage:

s0 = Sample.objects.create()
s1 = Sample(pk=s0.pk, name='Test 1')
s1.save()  # This will update the existing object instead of raising an IntegrityError

# To verify:
s0.refresh_from_db()
print(s0.name)  # This will print 'Test 1'
"""
