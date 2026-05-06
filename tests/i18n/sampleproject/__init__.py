import os
import sys
import subprocess

sys.path.insert(0, 'tests')
os.environ['PYTHONPATH'] = 'tests'

def run_makemigrations_check():
    result = subprocess.run(
        ["python", "tests/i18n/sampleproject/manage.py", "makemigrations", "--check"],
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr

if __name__ == "__main__":
    returncode, stdout, stderr = run_makemigrations_check()
    print(f"Return code: {returncode}")
    print(f"stdout: {stdout}")
    print(f"stderr: {stderr}")
    if returncode == 1:
        print("Test passed: makemigrations --check exited without creating migrations.")
    else:
        print("Test failed: makemigrations --check did not exit as expected.")
import subprocess

sys.path.insert(0, 'tests')

def run_makemigrations_check():
    result = subprocess.run(
        ["python", "tests/i18n/sampleproject/manage.py", "makemigrations", "--check"],
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr

if __name__ == "__main__":
    returncode, stdout, stderr = run_makemigrations_check()
    print(f"Return code: {returncode}")
    print(f"stdout: {stdout}")
    print(f"stderr: {stderr}")
    if returncode == 1:
        print("Test passed: makemigrations --check exited without creating migrations.")
    else:
        print("Test failed: makemigrations --check did not exit as expected.")
