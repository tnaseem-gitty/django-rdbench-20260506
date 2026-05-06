from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Test command for subparser functionality'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='subcommand', required=True)
        
        create_parser = subparsers.add_parser('create')
        create_parser.add_argument('name', help='Name for the created object')

    def handle(self, *args, **options):
        if options['subcommand'] == 'create':
            self.stdout.write(f"Creating object with name: {options['name']}")
        else:
            raise CommandError("Invalid subcommand")

