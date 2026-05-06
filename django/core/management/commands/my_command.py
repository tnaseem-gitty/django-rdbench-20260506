from django.core.management.base import BaseCommand, CommandError
from django.core.management import CommandParser

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser):
        shop = parser.add_mutually_exclusive_group(required=True)
        shop.add_argument('--shop-id', nargs='?', type=int, default=None, dest='shop_id')
        shop.add_argument('--shop', nargs='?', type=str, default=None, dest='shop_name')

    def handle(self, *args, **options):
        if options['shop_id']:
            self.stdout.write(f"Shop ID: {options['shop_id']}")
        elif options['shop_name']:
            self.stdout.write(f"Shop Name: {options['shop_name']}")
        else:
            raise CommandError("One of --shop-id or --shop is required")
