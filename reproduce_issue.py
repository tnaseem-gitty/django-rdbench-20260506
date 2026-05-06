import os
import django
from django.conf import settings
from django.db import models, connection
from django.test import TestCase

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
        ],
    )

django.setup()

class SimpleUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()

    class Meta:
        app_label = 'auth'

def create_user_table():
    with connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auth_simpleuser (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(150) UNIQUE NOT NULL,
                email VARCHAR(254) NOT NULL
            )
        ''')

class TestComposedQueries(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        create_user_table()

    def setUp(self):
        SimpleUser.objects.create(username='testuser', email='test@example.com')

    def test_composed_queries(self):
        qs1 = SimpleUser.objects.all()
        
        # Test with username and email
        result1 = qs1.union(qs1).values_list('username', 'email').get()
        print("Result 1:", result1)
        
        # Test with only email
        result2 = qs1.union(qs1).values_list('email').get()
        print("Result 2:", result2)

if __name__ == '__main__':
    test_case = TestComposedQueries()
    TestComposedQueries.setUpClass()
    test_case.setUp()
    test_case.test_composed_queries()
    print("Script completed successfully, no errors.")
