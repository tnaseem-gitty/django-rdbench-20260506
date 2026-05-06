from django.db import models

class Dimension(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.IntegerField()

# Simulate the database entries
Dimension.objects.bulk_create([
    Dimension(id=10, order=1),
    Dimension(id=11, order=2),
    Dimension(id=12, order=3),
    Dimension(id=13, order=4),
    Dimension(id=14, order=5),
    Dimension(id=15, order=6),
    Dimension(id=16, order=7),
    Dimension(id=17, order=8),
    Dimension(id=18, order=9),
])

# Reproduction of the issue
qs = (
    Dimension.objects.filter(pk__in=[10, 11])
    .union(Dimension.objects.filter(pk__in=[16, 17])
    .order_by('order'))
)

print(qs.order_by().values_list('pk', flat=True))
print([dim.id for dim in qs])
