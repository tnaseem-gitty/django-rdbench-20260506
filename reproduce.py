from django.db import models
from django.db.models import FilteredRelation, Q, F, Case, When

class MyNestedModel(models.Model):
    zone = models.CharField(max_length=100)
    is_all = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class MyModel(models.Model):
    zone = models.CharField(max_length=100)
    myrelation = models.ForeignKey(MyNestedModel, on_delete=models.CASCADE, related_name='nested')

qs = MyModel.objects.alias(
    relation_zone=FilteredRelation(
        "myrelation__nested",
        condition=Q(myrelation__nested__zone=F("zone"))
    ),
    relation_all=FilteredRelation(
        "myrelation__nested",
        condition=Q(myrelation__nested__is_all=True)
    ),
    price_zone=F("relation_zone__price")
).annotate(
    price_final=Case(
        When(
            price_zone__isnull=True,
            then=F("relation_all__price"),
        ),
        default=F("price_zone")
    )
)

print(str(qs.query))
