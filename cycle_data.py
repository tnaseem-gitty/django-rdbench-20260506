import logging
from django.core.management.base import BaseCommand
from treeherder.model.models import Job

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Cycle data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sleep-time',
            type=int,
            default=0,
            help='Time to sleep between cycles',
        )

    def handle(self, *args, **options):
        sleep_time = options['sleep_time']
        logger.info('Starting cycle_data with sleep_time=%d', sleep_time)
        Job.objects.cycle_data(sleep_time)
