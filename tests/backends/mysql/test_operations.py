from django.db import connection
from django.test import TestCase
from django.conf import settings
from django.db.backends.sqlite3.operations import DatabaseOperations

class SQLiteOperationsTests(TestCase):
    def test_datetime_cast_date_sql(self):
        ops = DatabaseOperations(connection=connection)

        # Save the original settings
        original_use_tz = settings.USE_TZ
        original_time_zone = connection.settings_dict.get('TIME_ZONE')

        try:
            settings.USE_TZ = True
            connection.settings_dict['TIME_ZONE'] = 'Europe/Paris'

            field_name = 'test_field'

            converted = ops.datetime_cast_date_sql(field_name, 'UTC')
            expected = "django_datetime_cast_date(test_field, 'UTC')"

            self.assertEqual(converted, expected)

        finally:
            # Restore the original settings
            settings.USE_TZ = original_use_tz
            if original_time_zone:
                connection.settings_dict['TIME_ZONE'] = original_time_zone
            else:
                connection.settings_dict.pop('TIME_ZONE', None)

print("Test file updated successfully.")
