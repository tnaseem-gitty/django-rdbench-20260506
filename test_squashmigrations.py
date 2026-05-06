from django.db.migrations.operations.models import CreateModel, AlterModelOptions

# Define a mock CreateModel operation
create_model_op = CreateModel(
    name="test_model",
    fields=[],
    options={"option1": "value1", "option2": "value2"},
    bases=(),
    managers=[]
)

# Define a mock AlterModelOptions operation that should clear options
alter_model_options_op = AlterModelOptions(
    name="test_model",
    options={"option1": "new_value1"}
)

# Apply the reduce method to simulate squashing migrations
reduced_ops = create_model_op.reduce(alter_model_options_op, "test_app")

# Check the resulting options in the reduced CreateModel operation
print(reduced_ops[0].options)  # Should print {'option1': 'new_value1'}
