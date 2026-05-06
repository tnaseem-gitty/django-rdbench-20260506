from django.utils.html import urlize

test_string = 'Search for google.com/?q=1&lt! and see.'
result = urlize(test_string)
print("Input:", test_string)
print("Output:", result)
print("Expected: Search for <a href=\"http://google.com/?q=1%3C\">google.com/?q=1&lt</a>! and see.")
