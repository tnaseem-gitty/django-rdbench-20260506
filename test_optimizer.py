from django.db import migrations, models
from django.db.migrations.optimizer import MigrationOptimizer

def test_optimizer():
    operations = [
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
    optimized = optimizer.optimize(operations, app_label="books")

    print(f"Original operations: {len(operations)}")
    print(f"Optimized operations: {len(optimized)}")
    
    for op in optimized:
        print(f"Operation: {op.__class__.__name__}")
        print(f"  Model: {op.model_name}")
        print(f"  Field: {op.name}")
        print(f"  Attributes: {op.field.deconstruct()[3]}")
        print()

if __name__ == "__main__":
    test_optimizer()
