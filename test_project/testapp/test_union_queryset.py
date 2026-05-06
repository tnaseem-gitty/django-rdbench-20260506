from django.test import TestCase
from .models import Dimension

class TestUnionQuerysetOrdering(TestCase):
    @classmethod
    def setUpTestData(cls):
        Dimension.objects.bulk_create([
            Dimension(id=10, name='A', order=1),
            Dimension(id=11, name='B', order=2),
            Dimension(id=16, name='C', order=3),
            Dimension(id=17, name='D', order=4),
        ])

    def test_union_queryset_ordering(self):
        qs1 = Dimension.objects.filter(pk__in=[10, 11])
        qs2 = Dimension.objects.filter(pk__in=[16, 17])
        
        print("qs1 query:", qs1.query)
        print("qs2 query:", qs2.query)
        
        qs = qs1.union(qs2).order_by('order')
        
        print("Union queryset query:", qs.query)
        print("Union queryset SQL:", qs.query.get_compiler(qs.db).as_sql())
        
        try:
            print("Initial queryset:", list(qs.values_list('id', flat=True)))
        except Exception as e:
            print(f"Exception raised during initial evaluation: {type(e).__name__}: {str(e)}")
        
        try:
            reordered = qs.order_by().values_list('pk', flat=True)
            print("Reordered queryset:", list(reordered))
        except Exception as e:
            print(f"Exception raised during reordering: {type(e).__name__}: {str(e)}")
        
        try:
            print("Trying to evaluate qs again:", list(qs))
        except Exception as e:
            print(f"Exception raised during final evaluation: {type(e).__name__}: {str(e)}")
        else:
            print("No exception was raised during final evaluation.")

        print("Test completed.")
