import datetime
import time
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0003_remove_testmodel_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='testmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
