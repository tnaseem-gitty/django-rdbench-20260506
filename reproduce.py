from django.db import models
from django.db.models import F

class ReservedName(models.Model):
    name = models.CharField(max_length=255)
    order = models.IntegerField()

ReservedName.objects.create(name='a', order=2)
qs1 = ReservedName.objects.all()
print(qs1.union(qs1).values_list('name', 'order').get())
print(qs1.union(qs1).values_list('order').get())
