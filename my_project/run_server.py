import os
import subprocess

def run_server(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()

# Run server with --noreload
stdout_noreload, stderr_noreload = run_server("python -X utf8 manage.py runserver 0.0.0.0:8005 -v3 --noreload")
print("Output with --noreload:")
print(stdout_noreload)
print(stderr_noreload)

# Run server without --noreload
stdout_reload, stderr_reload = run_server("python -X utf8 manage.py runserver 0.0.0.0:8005 -v3")
print("Output without --noreload:")
print(stdout_reload)
print(stderr_reload)
