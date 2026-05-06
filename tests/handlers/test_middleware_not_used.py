from django.core.exceptions import MiddlewareNotUsed
from django.core.handlers.base import BaseHandler
from django.test import SimpleTestCase
from django.http import HttpResponse

class DummyMiddleware:
    def __init__(self, get_response):
        raise MiddlewareNotUsed()

class MiddlewareNotUsedTests(SimpleTestCase):
    def test_middleware_not_used_handler_reset(self):
        class CustomHandler(BaseHandler):
            def load_middleware(self):
                self._middleware_chain = None
                handler = self._get_response
                for middleware in [DummyMiddleware]:
                    try:
                        mw_instance = middleware(handler)
                    except MiddlewareNotUsed:
                        continue
                    else:
                        handler = mw_instance
                return handler

            def _get_response(self, request):
                return HttpResponse("Test response")

        handler = CustomHandler()
        middleware_chain = handler.load_middleware()
        self.assertEqual(middleware_chain, handler._get_response)
