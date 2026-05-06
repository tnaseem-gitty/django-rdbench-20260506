from django.conf import settings
from django.http import HttpResponse
from django.test import SimpleTestCase

# Configure minimal Django settings
settings.configure(
    DEBUG=True,
    SECRET_KEY='secret',
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(),
)

class HttpResponseTest(SimpleTestCase):
    def test_http_response(self):
        # String content
        response = HttpResponse("My Content")
        print("String content:")
        print(response.content)

        # Bytes content
        response = HttpResponse(b"My Content")
        print("\nBytes content:")
        print(response.content)

        # memoryview content
        response = HttpResponse(memoryview(b"My Content"))
        print("\nmemoryview content:")
        print(response.content)

if __name__ == '__main__':
    from django.test.utils import setup_test_environment
    setup_test_environment()
    
    test = HttpResponseTest()
    test.test_http_response()
    
    print("\nScript completed successfully, no errors.")
