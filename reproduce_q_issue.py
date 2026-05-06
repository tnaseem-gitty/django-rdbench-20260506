from django.db.models import Q, Exists, OuterRef

class DummyExists(Exists):
    def __init__(self):
        super().__init__(OuterRef('dummy'))

print("Testing Q object with single key-value pair:")
print(Q(x=1).deconstruct())

print("\nTesting Q object with multiple key-value pairs:")
print(Q(x=1, y=2).deconstruct())

print("\nTesting Q object with Exists:")
try:
    print(Q(DummyExists()).deconstruct())
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")

print("\nScript completed successfully.")
