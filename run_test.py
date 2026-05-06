import os
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.test.utils import get_runner
from django.conf import settings
from tests.test_runner import setup

if __name__ == "__main__":
    setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True)
    failures = test_runner.run_tests(["responses.test_cookie.DeleteCookieTests.test_delete_cookie_preserves_samesite"])
    sys.exit(bool(failures))
