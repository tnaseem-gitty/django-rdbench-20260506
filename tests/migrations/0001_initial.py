from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OneModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oneval', models.BigIntegerField(null=True)),
                ('root', models.ForeignKey('self', null=True, on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='TwoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twoval', models.BigIntegerField(null=True)),
                ('record', models.ForeignKey('OneModel', on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
    ]
