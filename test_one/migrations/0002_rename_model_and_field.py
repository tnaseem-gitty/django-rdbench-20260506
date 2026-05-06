
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('test_one', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MyModel',
            new_name='MyModel2',
        ),
        migrations.RenameField(
            model_name='mymodel2',
            old_name='name',
            new_name='new_name',
        ),
    ]
