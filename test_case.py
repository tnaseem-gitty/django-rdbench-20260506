from django.test import TestCase
from django.db.models import Count
from test_models import Thing, Related

class IssueTestCase(TestCase):
    def setUp(self):
        t = Thing.objects.create()
        for _ in range(2):
            Related.objects.create(thing=t)

    def test_issue(self):
        print("Normal query:")
        print(Thing.objects.annotate(rc=Count('related')).order_by('rc').values('id', 'rc'))

        print("\nQuery with order_by('related'):")
        print(Thing.objects.annotate(rc=Count('related')).order_by('related').values('id', 'rc'))

        print("\nQuery with order_by('?'):")
        print(Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc'))

        print("\nSQL for order_by('?') query:")
        print(Thing.objects.annotate(rc=Count('related')).order_by('?').values('id', 'rc').query)
