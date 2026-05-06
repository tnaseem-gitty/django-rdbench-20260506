import os
import django
from django.db import models, migrations

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from app.models import TestConstraint

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestConstraint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_1', models.IntegerField(blank=True, null=True)),
                ('flag', models.BooleanField()),
            ],
        ),
        migrations.AddConstraint(
            model_name='testconstraint',
            constraint=models.CheckConstraint(
                check=models.Q(models.Q(('field_1__isnull', False), ('flag__exact', True)), ('flag__exact', False), _connector='OR'),
                name='field_1_has_value_if_flag_set'
            ),
        ),
    ]
print("Script completed successfully, no errors.")
