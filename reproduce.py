import os
import django
from django.core.management import call_command
from django.db import connection

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

# SQL commands to create the tables
create_tables_sql = """
CREATE TABLE foo (id serial primary key, other_id int UNIQUE);
CREATE TABLE bar (
    id serial primary key, other_id int,
    constraint myconst 
    FOREIGN KEY(other_id) references foo(other_id)
);
"""

# Execute the SQL commands
with connection.cursor() as cursor:
    cursor.execute(create_tables_sql)

# Run inspectdb command
call_command('inspectdb')

print("Script completed successfully, no errors.")
