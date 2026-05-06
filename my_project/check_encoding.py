import subprocess

def check_encoding(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode()

# Check encoding with -X utf8
stdout_utf8, stderr_utf8 = check_encoding("python -X utf8 -c 'with open(\"manage.py\", mode=\"r\") as stream: print(\"=== %s\" % stream.encoding)'")
print("Output with -X utf8:")
print(stdout_utf8)
print(stderr_utf8)

# Check encoding without -X utf8
stdout_default, stderr_default = check_encoding("python -c 'with open(\"manage.py\", mode=\"r\") as stream: print(\"=== %s\" % stream.encoding)'")
print("Output without -X utf8:")
print(stdout_default)
print(stderr_default)
