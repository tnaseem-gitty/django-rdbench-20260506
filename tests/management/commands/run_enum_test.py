from django.core.management.base import BaseCommand
from django.test.utils import get_runner
from django.conf import settings

class Command(BaseCommand):
    help = 'Runs the enum choices test'

    def handle(self, *args, **options):
        TestRunner = get_runner(settings)
        test_runner = TestRunner(verbosity=2, interactive=False)
        failures = test_runner.run_tests(["tests.test_enum_choices"])
        self.stdout.write(self.style.SUCCESS(f'Test failures: {failures}'))
