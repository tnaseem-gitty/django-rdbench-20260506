from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
