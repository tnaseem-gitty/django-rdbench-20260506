import subprocess
import time

with open('runserver_stdout.txt', 'w') as stdout, open('runserver_stderr.txt', 'w') as stderr:
    process = subprocess.Popen(['python', 'manage.py', 'runserver', '0:8000'], stdout=stdout, stderr=stderr)
    time.sleep(30)  # Run the server for 30 seconds
    process.terminate()
with open('runserver_stdout.txt', 'r') as stdout, open('runserver_stderr.txt', 'r') as stderr:
    print("STDOUT:")
    print(stdout.read())
    print("STDERR:")
    print(stderr.read())
