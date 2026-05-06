from django.db import models
import json

class TestModel(models.Model):
    json_field = models.JSONField()

# Create an instance of the model
instance = TestModel(json_field='中国')

# Serialize the instance
print(json.dumps(instance.json_field, ensure_ascii=False))
