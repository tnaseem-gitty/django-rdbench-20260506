import sys
import time
from django.core.management.commands.migrate import Command

class TestStdout:
    def __init__(self):
        self.content = []

    def write(self, message, ending=None):
        self.content.append(message)
        if ending:
            self.content.append(ending)
        sys.stdout.write(message + (ending or ''))
        sys.stdout.flush()

    def flush(self):
        sys.stdout.flush()

def test_migration_output():
    command = Command()
    command.stdout = TestStdout()
    command.verbosity = 2

    print("Starting test migration...")
    command.migration_progress_callback("apply_start", "test_migration")
    time.sleep(1)  # Simulate some work
    command.migration_progress_callback("apply_success", "test_migration")
    print("\nTest migration complete.")

    expected_output = [
        "  Applying test_migration...",
        " OK"
    ]

    actual_output = ''.join(command.stdout.content)
    if all(expected in actual_output for expected in expected_output):
        print("Test passed: All expected output was present and flushed correctly.")
    else:
        print("Test failed: Some expected output was missing or not flushed.")
        print("Actual output:", actual_output)

if __name__ == "__main__":
    test_migration_output()
