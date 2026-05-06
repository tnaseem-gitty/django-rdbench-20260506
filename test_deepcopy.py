import copy

class Field:
    def __init__(self):
        self.error_messages = {'required': 'This field is required.'}

    def __deepcopy__(self, memo):
        result = copy.copy(self)
        memo[id(self)] = result
        result.error_messages = copy.deepcopy(self.error_messages, memo)
        return result

# Create two instances of the field
field1 = Field()
field2 = copy.deepcopy(field1)

# Modify error message in field1
field1.error_messages['required'] = 'Custom error message for field1'

# Check if the error message in field2 remains unchanged
print("Field1 error message:", field1.error_messages['required'])
print("Field2 error message:", field2.error_messages['required'])

if field1.error_messages['required'] != field2.error_messages['required']:
    print("Test passed: Error messages are different after modification")
else:
    print("Test failed: Error messages are the same after modification")

print("Script completed successfully, no errors.")
