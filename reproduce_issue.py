from django.utils.encoding import force_str

def add(value, arg):
    """Add the arg to the value."""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        try:
            return force_str(value) + force_str(arg)
        except Exception:
            return ''

# Simulating lazy string
class LazyString:
    def __init__(self, string):
        self.string = string
    def __str__(self):
        return self.string

# Test cases
print("Test 1 (string + lazy string):")
print(add('Hello, ', LazyString('Lazy World')))

print("\nTest 2 (lazy string + string):")
print(add(LazyString('Lazy World'), ' Hello'))

print("\nTest 3 (string + regular string):")
print(add('Hello, ', 'Regular World'))

print("\nTest 4 (string + string, no lazy strings):")
print(add('Hello, ', 'World'))

print("\nTest 5 (int + int):")
print(add(1, 2))

print("\nTest 6 (string + int):")
print(add('Hello, ', 5))

print("\nTest 7 (int + string):")
print(add(5, ' World'))

print("\nScript completed.")
