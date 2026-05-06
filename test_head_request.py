import io
import os
import sys
from django.conf import settings
from django.core.servers.basehttp import ServerHandler
from django.http import HttpResponse
from django.core.wsgi import get_wsgi_application
import socketserver

# Configure Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'django.conf.global_settings'
settings.configure()

def test_head_request():
    def simple_app(environ, start_response):
        response = HttpResponse("Hello, World!")
        status = f'{response.status_code} {response.reason_phrase}'
        headers = [(name, value) for name, value in response.items()]
        start_response(status, headers)
        return [response.content]

    environ = {
        'REQUEST_METHOD': 'HEAD',
        'wsgi.input': io.BytesIO(),
        'wsgi.errors': io.StringIO(),
        'SERVER_NAME': 'testserver',
        'SERVER_PORT': '80',
        'SERVER_PROTOCOL': 'HTTP/1.1',
    }

    stdout = io.BytesIO()
    stderr = io.StringIO()

    class MockServer(socketserver.ThreadingMixIn):
        pass

    class MockRequestHandler:
        command = 'HEAD'
        server = MockServer()
        def log_request(self, *args, **kwargs):
            pass

    handler = ServerHandler(
        stdin=environ['wsgi.input'],
        stdout=stdout,
        stderr=stderr,
        environ=environ,
    )
    handler.request_handler = MockRequestHandler()

    handler.run(simple_app)

    response = stdout.getvalue().decode('utf-8')
    error = stderr.getvalue()
    
    print("Response:")
    print(response)
    
    if error:
        print("Error:", file=sys.stderr)
        print(error, file=sys.stderr)

    assert '200 OK' in response, f"Expected 200 OK, but got: {response.splitlines()[0] if response else 'No response'}"
    assert 'Content-Length' in response
    assert 'Hello, World!' not in response, "Body should not be present in HEAD response"

if __name__ == '__main__':
    test_head_request()
    print("Test passed successfully!")
