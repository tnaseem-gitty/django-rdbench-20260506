import django_setup
from django.core.management import call_command
from test_case import IssueTestCase

def run_tests():
    call_command('migrate')
    test_case = IssueTestCase()
    test_case.setUp()
    test_case.test_issue()
    print("\nScript completed successfully, no errors.")

if __name__ == '__main__':
    run_tests()
