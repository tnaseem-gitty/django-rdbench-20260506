import re

def simulate_runserver(address):
    if address == "0:8000":
        address = "0.0.0.0:8000"
    print(f"Starting development server at http://{address}/")

simulate_runserver("0:8000")
