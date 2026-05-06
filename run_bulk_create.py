import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')
django.setup()

# Run migrations
call_command('migrate', interactive=False)

from app.models import ActivityBlackListed

# Assuming instances is a list of ActivityBlackListed objects
instances = [
    ActivityBlackListed(blacklistid=1, sectorid=10),
    ActivityBlackListed(blacklistid=2, sectorid=20),
    # other instances...
]

ActivityBlackListed.objects.bulk_create(instances, update_conflicts=True, update_fields=["sectorid"], unique_fields=["blacklistid"])

print("Script completed successfully, no errors.")
