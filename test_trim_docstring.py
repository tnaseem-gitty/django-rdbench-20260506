from django.contrib.admindocs.utils import trim_docstring

def test_trim_docstring():
    # Test case 1: Docstring with first line not empty
    docstring1 = '''This is a test docstring.
    It has multiple lines.
    The first line is not empty.'''
    print("Test case 1:")
    print(trim_docstring(docstring1))
    print()

    # Test case 2: Docstring with first line empty
    docstring2 = '''
    This is another test docstring.
    It also has multiple lines.
    The first line is empty.'''
    print("Test case 2:")
    print(trim_docstring(docstring2))
    print()

    # Test case 3: Single line docstring
    docstring3 = '''Single line docstring.'''
    print("Test case 3:")
    print(trim_docstring(docstring3))
    print()

if __name__ == "__main__":
    test_trim_docstring()
