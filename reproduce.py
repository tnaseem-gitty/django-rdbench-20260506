from django.db import migrations, models
from django.db.migrations.optimizer import MigrationOptimizer

operations = [
    migrations.AddField(
        model_name="book",
        name="title",
        field=models.CharField(max_length=256, null=True),
    ),
    migrations.AlterField(
        model_name="book",
        name="title",
        field=models.CharField(max_length=128, null=True),
    ),
    migrations.AlterField(
        model_name="book",
        name="title",
        field=models.CharField(max_length=128, null=True, help_text="help"),
    ),
    migrations.AlterField(
        model_name="book",
        name="title",
        field=models.CharField(max_length=128, null=True, help_text="help", default=None),
    ),
]

optimizer = MigrationOptimizer()
optimized_operations = optimizer.optimize(operations[1:], "books")
for op in optimized_operations:
    print(op)
