from django.contrib.admindocs.utils import trim_docstring

def test():
    """test tests something.
    """
    docstring = test.__doc__
    trimmed = trim_docstring(docstring)
    print(trimmed)

test()
