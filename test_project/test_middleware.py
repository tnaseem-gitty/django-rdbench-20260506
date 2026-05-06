import os
import django
from django.test import AsyncClient
import asyncio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

async def test_middleware():
    client = AsyncClient()
    response = await client.get('/')
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.content}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_middleware())
    loop.close()
