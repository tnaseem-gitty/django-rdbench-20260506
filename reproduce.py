from django.utils.deprecation import MiddlewareMixin
from django.core.handlers.asgi import ASGIRequest
from django.http.response import HttpResponse
import uvicorn
from django.conf import settings
from django.core.asgi import get_asgi_application

class DummyMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        print(request.__class__, response.__class__)
        return response

if not settings.configured:
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        MIDDLEWARE=[
            'reproduce.DummyMiddleware',
            'django.middleware.security.SecurityMiddleware',
        ],
        ALLOWED_HOSTS=['*'],
    )

application = get_asgi_application()

if __name__ == "__main__":
    uvicorn.run(application, host="127.0.0.1", port=8000)
