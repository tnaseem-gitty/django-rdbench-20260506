import re

def replace_named_groups(pattern):
    return re.sub(r'\(\?P<\w+>', '(', pattern)

pattern = r'entries/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)'
print(replace_named_groups(pattern))
