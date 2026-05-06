import subprocess

def run_server(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()

# Run server with -X utf8
stdout_utf8, stderr_utf8 = run_server("python -X utf8 manage.py runserver 0.0.0.0:8005 -v3")
print("Output with -X utf8:")
print(stdout_utf8)
print(stderr_utf8)
