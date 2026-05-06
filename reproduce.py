from django.db.models import ExpressionWrapper, IntegerField, Value, Sum
from tests.expressions.models import Number

def execQuery(expr):
    expr = ExpressionWrapper(expr, output_field=IntegerField())
    return Number.objects.annotate(expr_res=expr).values('expr_res', 'integer').annotate(sum=Sum('float'))

# Example usage
queryset = execQuery(Value(3))
print(queryset.query)
