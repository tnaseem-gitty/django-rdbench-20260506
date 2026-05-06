from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testmodel',
            options={
                'unique_together': {('field1', 'field2')},
            },
        ),
    ]
