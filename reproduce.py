from django.utils.html import urlize

test_string = 'Search for google.com/?q=1&lt! and see.'
expected_output = 'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.'
actual_output = urlize(test_string)

print("Expected:", expected_output)
print("Actual:", actual_output)
