from django.utils.decorators import sync_and_async_middleware
import asyncio

@sync_and_async_middleware
class DummyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    async def __call__(self, request):
        if asyncio.iscoroutinefunction(self.get_response):
            response = await self.get_response(request)
        else:
            response = self.get_response(request)
        
        if asyncio.iscoroutine(response):
            response = await response
        
        print(f"Request: {request.__class__}, Response: {response.__class__}")
        return response
