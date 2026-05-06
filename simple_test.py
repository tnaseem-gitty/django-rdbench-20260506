from django.utils.deprecation import MiddlewareMixin
from django.core.handlers.asgi import ASGIRequest
from django.http.response import HttpResponse
import asyncio
import io

class DummyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        print(request.__class__, response.__class__)
        return response

async def dummy_coroutine():
    return HttpResponse("Dummy response")
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        ALLOWED_HOSTS=['*'],
        DEFAULT_CHARSET='utf-8',
    )
django.setup()

request = ASGIRequest({
    'type': 'http',
    'method': 'GET',
    'path': '/',
    'headers': [],
}, io.BytesIO(b''))
middleware = DummyMiddleware()
loop = asyncio.get_event_loop()
response = loop.run_until_complete(dummy_coroutine())
middleware.process_response(request, response)
