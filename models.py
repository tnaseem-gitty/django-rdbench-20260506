import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Foo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        app_label = '__main__'

class Bar(models.Model):
    foo_content_type = models.ForeignKey(
        ContentType, related_name='actor',
        on_delete=models.CASCADE, db_index=True
    )
    foo_object_id = models.CharField(max_length=255, db_index=True)
    foo = GenericForeignKey('foo_content_type', 'foo_object_id')

    class Meta:
        app_label = '__main__'
from models import Foo, Bar
