from django.db import models, migrations
from django.test import TestCase
from django.db.utils import IntegrityError

class FooBar(models.Model):
    id = models.AutoField(primary_key=True)
    class Meta:
        unique_together = (('id',),)

class TestUniqueTogether(TestCase):
    def test_drop_unique_together(self):
        # Create the initial migration
        initial_migration = migrations.CreateModel(
            name='FooBar',
            fields=[
                ('id', models.AutoField(primary_key=True)),
            ],
            options={
                'unique_together': {('id',)},
            },
        )

        # Apply the initial migration
        with self.assertRaises(IntegrityError):
            initial_migration.apply(None, None)

        # Create the migration to drop the unique_together constraint
        drop_unique_together_migration = migrations.AlterUniqueTogether(
            name='foobar',
            unique_together=set(),
        )

        # Apply the migration to drop the unique_together constraint
        drop_unique_together_migration.apply(None, None)

        # Verify that the unique_together constraint has been dropped
        with self.assertRaises(IntegrityError):
            FooBar.objects.create(id=1)
            FooBar.objects.create(id=1)

print("Script completed successfully, no errors.")
