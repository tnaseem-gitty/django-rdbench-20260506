from django.db import models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.test import SimpleTestCase


class SchemaEditorTests(SimpleTestCase):

    def test_effective_default_callable(self):
        """SchemaEditor.effective_default() shouldn't call callable defaults."""
        class MyStr(str):
            def __call__(self):
                return self

        class MyCharField(models.CharField):
            def _get_default(self):
                return self.default

        field = MyCharField(max_length=1, default=MyStr)
        self.assertEqual(BaseDatabaseSchemaEditor._effective_default(field), MyStr)

    def test_delete_composed_index_multiple_constraints(self):
        class MockField:
            def __init__(self, column):
                self.column = column

        class MockMeta:
            def get_field(self, field_name):
                return MockField(field_name)

        class MockModel:
            _meta = MockMeta()
            _meta.db_table = 'test_table'
            _meta.constraints = []
            _meta.indexes = []

        class MockConnection:
            class features:
                can_rollback_ddl = False

        class MockSchemaEditor(BaseDatabaseSchemaEditor):
            executed_statements = []

            def execute(self, sql, params=None):
                self.executed_statements.append(sql)

            def _constraint_names(self, model, column_names=None, unique=None, primary_key=None, index=None, foreign_key=None, check=None, type_=None, exclude=None):
                return ['constraint1', 'constraint2']

            def _delete_constraint_sql(self, template, model, name):
                return f"DROP CONSTRAINT {name}"

        model = MockModel()
        connection = MockConnection()
        editor = MockSchemaEditor(connection=connection)
        editor._delete_composed_index(model, ['field1', 'field2'], {'unique': True}, "DROP INDEX")

        self.assertEqual(len(editor.executed_statements), 2)
        self.assertEqual(editor.executed_statements[0], "DROP CONSTRAINT constraint1")
        self.assertEqual(editor.executed_statements[1], "DROP CONSTRAINT constraint2")
