import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
django.setup()

from django.db.models import F
from test_app.models import OneModel, TwoModel

# Test cases
def test_queries():
    # Case 1: Unexpected DESC ordering
    qs1 = TwoModel.objects.filter(record__oneval__in=[1,2,3])
    qs1 = qs1.order_by("record__root_id")
    print("Query 1:")
    print(qs1.query)
    print()

    # Case 2: Correct ordering
    qs2 = TwoModel.objects.filter(record__oneval__in=[1,2,3])
    qs2 = qs2.order_by("record__root__id")
    print("Query 2:")
    print(qs2.query)
    print()

    # Case 3: Workaround with annotation
    qs3 = TwoModel.objects.filter(record__oneval__in=[1,2,3])
    qs3 = qs3.annotate(root_id=F("record__root_id"))
    qs3 = qs3.order_by("root_id")
    print("Query 3:")
    print(qs3.query)
    print()

    # Case 4: Inverted sort order
    qs4 = TwoModel.objects.filter(record__oneval__in=[1,2,3])
    qs4 = qs4.order_by("-record__root_id")
    print("Query 4:")
    print(qs4.query)
    print()

if __name__ == "__main__":
    from django.core.management import call_command
    call_command('makemigrations', interactive=False)
    call_command('migrate', interactive=False)
    test_queries()

print("Script completed successfully, no errors.")
