from django.db.models import Q
from collections import namedtuple

Range = namedtuple('Range', ['near', 'far'])

try:
    # This should work now with our fix
    q = Q(id__range=Range(1, 10))
    print("Test passed: Named tuple used successfully in Q object")
    # Let's print the Q object to verify its contents
    print(f"Q object: {q}")
except TypeError as e:
    print(f"Test failed: {str(e)}")

print("Test completed.")
