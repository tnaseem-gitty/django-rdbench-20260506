import os
import django

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
django.setup()

from django.test import TestCase
from testapp import Dimension

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
        qs = (
            Dimension.objects.filter(pk__in=[10, 11])
            .union(Dimension.objects.filter(pk__in=[16, 17]))
            .order_by('order')
        )
        
        print("Initial queryset:", [d.id for d in qs])
        
        try:
            reordered = qs.order_by().values_list('pk', flat=True)
            print("Reordered queryset:", list(reordered))
            
            # This should raise an exception
            print("Trying to evaluate qs again:", [d.id for d in qs])
        except Exception as e:
            print(f"Exception raised: {type(e).__name__}: {str(e)}")

        print("Test completed.")

if __name__ == '__main__':
    test_case = TestUnionQuerysetOrdering()
    test_case.setUpTestData()
    test_case.test_union_queryset_ordering()
