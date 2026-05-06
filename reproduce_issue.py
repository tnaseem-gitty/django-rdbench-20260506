import os
import django
from django.conf import settings
from django.db import models
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from datetime import timedelta

def configure_settings():
    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'reproduce_issue',
            ],
            USE_TZ=False,
        )
    django.setup()

def define_model():
    # Define a simple model
    class TestModel(models.Model):
        duration = models.DurationField()

        class Meta:
            app_label = 'reproduce_issue'
    
    return TestModel

def serialize_timedelta(td, precision="milliseconds"):
    if precision == "milliseconds":
        return int(td.total_seconds() * 1000)
    else:
        raise ValueError("Unsupported precision")

# Create the test query
def run_test_query(TestModel):
    from django.core.management import call_command
    from django.db import connection
    from django.db.migrations.executor import MigrationExecutor

    # Create a migration for our model
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(TestModel)

    # Apply migrations
    executor = MigrationExecutor(connection)
    executor.migrate([])

    # Insert some test data
    TestModel.objects.create(duration=timedelta(milliseconds=345))
    TestModel.objects.create(duration=timedelta(milliseconds=678))
    TestModel.objects.create(duration=timedelta(milliseconds=901))

    for obj in TestModel.objects.all():
        serialized = serialize_timedelta(obj.duration)
        print(f"Original: {obj.duration.total_seconds() * 1000}ms, Serialized: {serialized}ms")

    aggregate = TestModel.objects.aggregate(
        total_duration=Sum("duration")
    )
    print("Query executed successfully")
    print(f"Total duration: {aggregate['total_duration'].total_seconds() * 1000}ms")

if __name__ == "__main__":
    configure_settings()
    TestModel = define_model()
    run_test_query(TestModel)
