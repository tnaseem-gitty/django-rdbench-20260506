from django.core.management.base import BaseCommand
from django.test.utils import setup_test_environment
from django.test.runner import DiscoverRunner

class Command(BaseCommand):
    help = 'Runs the admin search test'

    def handle(self, *args, **options):
        setup_test_environment()
        test_runner = DiscoverRunner(verbosity=2)
        test_labels = ['django.contrib.admin.test_admin_search']
        test_runner.run_tests(test_labels)
