
from django.db.models import DecimalField, IntegerField
from django.db.models.functions import Mod
from decimal import Decimal

def test_mod_function():
    decimal_field = DecimalField(max_digits=10, decimal_places=2)
    integer_field = IntegerField()

    # Test Decimal MOD Integer
    result = Mod(decimal_field, integer_field).resolve_expression()
    assert isinstance(result.output_field, DecimalField), 'Decimal MOD Integer should return DecimalField'
    
    # Test Integer MOD Decimal
    result = Mod(integer_field, decimal_field).resolve_expression()
    assert isinstance(result.output_field, DecimalField), 'Integer MOD Decimal should return DecimalField'
    
    # Test Integer MOD Integer
    result = Mod(integer_field, integer_field).resolve_expression()
    assert isinstance(result.output_field, IntegerField), 'Integer MOD Integer should return IntegerField'

    print('All tests passed successfully!')

if __name__ == '__main__':
    import django
    django.setup()
    test_mod_function()

