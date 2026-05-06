from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Test the --skip-checks option'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-checks',
            action='store_true',
            help='Skip system checks.',
        )

    def handle(self, *args, **options):
        if options['skip_checks']:
            self.stdout.write('System checks skipped.')
        else:
            self.stdout.write('System checks not skipped.')
