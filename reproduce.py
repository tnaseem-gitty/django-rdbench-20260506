from decimal import Decimal
from django.conf import settings

# Configure minimal Django settings
settings.configure(USE_L10N=False, USE_THOUSAND_SEPARATOR=False)

from django.utils.numberformat import format as nformat

print("Testing with 2 decimal places:")
print(f"1e-199: {nformat(Decimal('1e-199'), '.', decimal_pos=2)}")
print(f"1e-200: {nformat(Decimal('1e-200'), '.', decimal_pos=2)}")
print(f"1e-201: {nformat(Decimal('1e-201'), '.', decimal_pos=2)}")
print(f"0.01: {nformat(Decimal('0.01'), '.', decimal_pos=2)}")
print(f"0.001: {nformat(Decimal('0.001'), '.', decimal_pos=2)}")

print("\nTesting with 4 decimal places:")
print(f"1e-199: {nformat(Decimal('1e-199'), '.', decimal_pos=4)}")
print(f"1e-200: {nformat(Decimal('1e-200'), '.', decimal_pos=4)}")
print(f"1e-201: {nformat(Decimal('1e-201'), '.', decimal_pos=4)}")
print(f"0.0001: {nformat(Decimal('0.0001'), '.', decimal_pos=4)}")
print(f"0.00001: {nformat(Decimal('0.00001'), '.', decimal_pos=4)}")

print("\nScript completed successfully, no errors.")
