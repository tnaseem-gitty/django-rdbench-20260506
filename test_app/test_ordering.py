from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import SystemCheckError
from django.db.models import CheckConstraint, Q
from django.db.models.fields import FieldError
from django.test.utils import override_system_checks
from .models import TestModel, ValidTestModel
from datetime import timedelta
import io
from contextlib import redirect_stdout, redirect_stderr

class TestModelOrderingTestCase(TestCase):
    @override_system_checks([])
    def test_invalid_ordering_with_pk(self):
        # Capture both stdout and stderr
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err), self.assertRaises(SystemCheckError):
            call_command('check', 'test_app')
        
        # Check if the error output contains the expected error message
        error_output = err.getvalue()
        self.assertIn("E015", error_output, "Expected validation error E015 not found")
        self.assertIn("'ordering' refers to the nonexistent field, related field, or lookup 'td_field__pk'", error_output)

    def test_valid_ordering_without_pk(self):
        # This should work without raising an exception
        test_model = ValidTestModel(td_field=timedelta(milliseconds=345))
        try:
            test_model.full_clean()
            test_model.save()
        except ValidationError as e:
            self.fail(f"Unexpected ValidationError raised: {str(e)}")

        self.assertTrue(True, "No exception raised when using 'td_field' in ordering")

    @override_system_checks([])
    def test_query_with_invalid_ordering(self):
        # This should raise a FieldError when trying to query with the invalid ordering
        with self.assertRaises(FieldError):
            list(TestModel.objects.all())
