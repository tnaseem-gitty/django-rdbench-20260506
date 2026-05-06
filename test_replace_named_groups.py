from django.contrib.admindocs.utils import replace_named_groups

def test_replace_named_groups():
    # Test case 1: Pattern with trailing slash
    pattern1 = r'entries/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)/'
    expected1 = r'entries/<pk>/relationships/<related_field>/'
    assert replace_named_groups(pattern1) == expected1, f"Test case 1 failed. Expected {expected1}, got {replace_named_groups(pattern1)}"

    # Test case 2: Pattern without trailing slash (the problematic case)
    pattern2 = r'entries/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)'
    expected2 = r'entries/<pk>/relationships/<related_field>'
    assert replace_named_groups(pattern2) == expected2, f"Test case 2 failed. Expected {expected2}, got {replace_named_groups(pattern2)}"

    # Test case 3: Pattern with nested groups
    pattern3 = r'^(?P<a>(x|y))/b/(?P<c>\w+)$'
    expected3 = r'^<a>/b/<c>$'
    assert replace_named_groups(pattern3) == expected3, f"Test case 3 failed. Expected {expected3}, got {replace_named_groups(pattern3)}"

    print("All test cases passed successfully!")

if __name__ == "__main__":
    test_replace_named_groups()
