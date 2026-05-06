from django.db.models import Value, ExpressionWrapper, IntegerField, Sum
from django.test import TransactionTestCase, override_settings
from django.db import connection

from .models import Company, Employee, Manager


@override_settings(INSTALLED_APPS=['tests.expressions'])
class ConstantExpressionsTests(TransactionTestCase):
    available_apps = ['tests.expressions']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Ensure the models are created in the test database
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(Manager)
            schema_editor.create_model(Employee)
            schema_editor.create_model(Company)

    def setUp(self):
        # Create Manager instances first
        manager1 = Manager.objects.create(name='Manager 1')
        manager2 = Manager.objects.create(name='Manager 2')
        manager3 = Manager.objects.create(name='Manager 3')

        # Create Employee instances
        employee1 = Employee.objects.create(firstname='John', lastname='Doe', manager=manager1)
        employee2 = Employee.objects.create(firstname='Jane', lastname='Smith', manager=manager2)
        employee3 = Employee.objects.create(firstname='Bob', lastname='Johnson', manager=manager3)

        # Now create Company instances with valid employee IDs
        Company.objects.create(name='Example Inc.', num_employees=2300, num_chairs=5, ceo=employee1)
        Company.objects.create(name='Foobar Ltd.', num_employees=3, num_chairs=4, ceo=employee2)
        Company.objects.create(name='Test GmbH', num_employees=32, num_chairs=1, ceo=employee3)

    def test_constant_expression_in_group_by(self):
        # This query should not include the constant expression in the GROUP BY clause
        expr = ExpressionWrapper(Value(3), output_field=IntegerField())
        qs = Company.objects.annotate(
            const=expr
        ).values('const', 'name').annotate(
            total_employees=Sum('num_employees')
        )

        # Check that the query executes without error
        result = list(qs)

        # Verify the results
        expected = [
            {'const': 3, 'name': 'Example Inc.', 'total_employees': 2300},
            {'const': 3, 'name': 'Foobar Ltd.', 'total_employees': 3},
            {'const': 3, 'name': 'Test GmbH', 'total_employees': 32},
        ]
        self.assertEqual(result, expected)

        # Print the SQL query for debugging
        sql = str(qs.query)
        print(f"Generated SQL: {sql}")

        # Check that the constant expression is not in the GROUP BY clause
        self.assertNotIn('3', sql[sql.index('GROUP BY'):])
    @classmethod
    def tearDownClass(cls):
        # Clean up the created tables
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(Company)
            schema_editor.delete_model(Employee)
            schema_editor.delete_model(Manager)
        super().tearDownClass()
