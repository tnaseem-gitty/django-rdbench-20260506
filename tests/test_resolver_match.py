import functools
from django.urls.resolvers import ResolverMatch

def test_function(a, b, c=3):
    return a + b + c

def test_resolver_match():
    # Test with regular function
    regular_match = ResolverMatch(test_function, (1, 2), {}, url_name='test')
    print(repr(regular_match))

    # Test with partial function
    partial_func = functools.partial(test_function, b=5, c=10)
    partial_match = ResolverMatch(partial_func, (1,), {}, url_name='test_partial')
    print(repr(partial_match))

if __name__ == '__main__':
    test_resolver_match()
