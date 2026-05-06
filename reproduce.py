from django.http import FileResponse

# Test for .Z file extension
response_z = FileResponse(open('test.html.Z', 'rb'))
print(f"Content-Type for .Z file: {response_z['Content-Type']}")

# Test for .br file extension
response_br = FileResponse(open('test.html.br', 'rb'))
print(f"Content-Type for .br file: {response_br['Content-Type']}")
