from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
import re

def test_validators():
    ascii_validator = ASCIIUsernameValidator()
    unicode_validator = UnicodeUsernameValidator()

    valid_username = "valid_username"
    invalid_username = "invalid_username\n"

    print("Testing ASCIIUsernameValidator:")
    print("Valid username: {}".format(bool(re.match(ascii_validator.regex, valid_username))))
    print("Invalid username: {}".format(bool(re.match(ascii_validator.regex, invalid_username))))

    print("\nTesting UnicodeUsernameValidator:")
    print("Valid username: {}".format(bool(re.match(unicode_validator.regex, valid_username))))
    print("Invalid username: {}".format(bool(re.match(unicode_validator.regex, invalid_username))))

if __name__ == "__main__":
    test_validators()

print("Script completed successfully, no errors.")
