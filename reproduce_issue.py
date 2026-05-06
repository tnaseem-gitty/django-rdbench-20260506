# Mock Q class
class Q:
    def __init__(self):
        self.value = "Q"

    def __and__(self, other):
        return f"({self.value} AND {other})"

    def __rand__(self, other):
        return f"({other} AND {self.value})"

    def __repr__(self):
        return self.value

# Mock Exists class
class MockExists:
    def __init__(self):
        self.value = "Exists"

    def __and__(self, other):
        return f"({self.value} AND {other})"

    def __rand__(self, other):
        return f"({other} AND {self.value})"

    def __repr__(self):
        return self.value

# Test case 1: MockExists() & Q()
result1 = MockExists() & Q()
print("MockExists() & Q():", result1)

# Test case 2: Q() & MockExists()
result2 = Q() & MockExists()
print("Q() & MockExists():", result2)

print("Script completed successfully.")
