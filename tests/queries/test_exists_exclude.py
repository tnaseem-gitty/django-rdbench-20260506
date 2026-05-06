import django
from django.conf import settings

if not settings.configured:
    settings.configure()

django.setup()

from django.db.models import Exists, OuterRef, Q
from tests.queries.models import Number, Item

def test_exists_exclude(self):
    # filter()
    qs = Number.objects.annotate(
        foo=Exists(
            Item.objects.filter(tags__category_id=OuterRef('pk'))
        )
    ).filter(foo=True)
    print(qs) # works
    # exclude()
    qs = Number.objects.annotate(
        foo=Exists(
            Item.objects.exclude(tags__category_id=OuterRef('pk'))
        )
    ).filter(foo=True)
    print(qs) # crashes
    # filter(~Q())
    qs = Number.objects.annotate(
        foo=Exists(
            Item.objects.filter(~Q(tags__category_id=OuterRef('pk')))
        )
    ).filter(foo=True)
    print(qs) # crashes
