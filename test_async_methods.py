import asyncio
from django.db import models
from asgiref.sync import sync_to_async

# Define test models
class Parent(models.Model):
    name = models.CharField(max_length=100)

class Child(models.Model):
    parent = models.ForeignKey(Parent, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

# Define test functions
async def test_acreate():
    parent = await sync_to_async(Parent.objects.create)(name="Parent1")
    child = await parent.children.acreate(name="Child1")
    print("acreate:", child)

async def test_aget_or_create():
    parent = await sync_to_async(Parent.objects.create)(name="Parent2")
    child, created = await parent.children.aget_or_create(name="Child2")
    print("aget_or_create:", child, "Created:", created)

async def test_aupdate_or_create():
    parent = await sync_to_async(Parent.objects.create)(name="Parent3")
    child, created = await parent.children.aupdate_or_create(name="Child3")
    print("aupdate_or_create:", child, "Created:", created)

# Run tests
async def main():
    await test_acreate()
    await test_aget_or_create()
    await test_aupdate_or_create()

asyncio.run(main())
