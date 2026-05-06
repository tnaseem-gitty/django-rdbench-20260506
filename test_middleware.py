from django.utils.deprecation import MiddlewareMixin
from django.core.handlers.asgi import ASGIRequest
from django.http.response import HttpResponse
from django.conf import settings
from django.core.asgi import get_asgi_application
import asyncio

class DummyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        print(request.__class__, response.__class__)
        return response

if not settings.configured:
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        MIDDLEWARE=[
            'test_middleware.DummyMiddleware',
            'django.middleware.security.SecurityMiddleware',
        ],
        ALLOWED_HOSTS=['*'],
    )

application = get_asgi_application()

async def test_request():
    scope = {
        'type': 'http',
        'method': 'GET',
        'path': '/',
        'headers': [],
    }
    receive = asyncio.Queue()
    send = asyncio.Queue()
    await application(scope, receive.get, send.put)
    while not send.empty():
        message = await send.get()
        print(message)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_request())
