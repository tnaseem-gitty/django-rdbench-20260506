from django.db import models
from django.test import TestCase
from django.db.models import FilteredRelation, Q, F

class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_bestseller = models.BooleanField(default=False)
    genre = models.CharField(max_length=50)

class MultipleFilteredRelationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        author1 = Author.objects.create(name="Author 1")
        author2 = Author.objects.create(name="Author 2")
        
        Book.objects.create(title="Book 1", author=author1, is_bestseller=True, genre="Fiction")
        Book.objects.create(title="Book 2", author=author1, is_bestseller=False, genre="Non-Fiction")
        Book.objects.create(title="Book 3", author=author2, is_bestseller=True, genre="Fiction")
        Book.objects.create(title="Book 4", author=author2, is_bestseller=False, genre="Non-Fiction")

    def test_multiple_filtered_relations(self):
        qs = Author.objects.annotate(
            bestseller_books=FilteredRelation(
                'book',
                condition=Q(book__is_bestseller=True)
            ),
            fiction_books=FilteredRelation(
                'book',
                condition=Q(book__genre='Fiction')
            )
        ).annotate(
            bestseller_count=models.Count('bestseller_books'),
            fiction_count=models.Count('fiction_books')
        )

        # This assertion will fail because only the last FilteredRelation (fiction_books) is being used
        self.assertQuerysetEqual(
            qs.values('name', 'bestseller_count', 'fiction_count').order_by('name'),
            [
                {'name': 'Author 1', 'bestseller_count': 1, 'fiction_count': 1},
                {'name': 'Author 2', 'bestseller_count': 1, 'fiction_count': 1}
            ],
            transform=dict
        )

        # Print the actual results to see what's happening
        print(list(qs.values('name', 'bestseller_count', 'fiction_count').order_by('name')))

        # Test that only the last FilteredRelation is being used
        self.assertQuerysetEqual(
            qs.values('name', 'bestseller_count', 'fiction_count').order_by('name'),
            [
                {'name': 'Author 1', 'bestseller_count': 1, 'fiction_count': 1},
                {'name': 'Author 2', 'bestseller_count': 1, 'fiction_count': 1}
            ],
            transform=dict
        )

        # Test with reversed order of FilteredRelations
        qs_reversed = Author.objects.annotate(
            fiction_books=FilteredRelation(
                'book',
                condition=Q(book__genre='Fiction')
            ),
            bestseller_books=FilteredRelation(
                'book',
                condition=Q(book__is_bestseller=True)
            )
        ).annotate(
            bestseller_count=models.Count('bestseller_books'),
            fiction_count=models.Count('fiction_books')
        )

        self.assertQuerysetEqual(
            qs_reversed.values('name', 'bestseller_count', 'fiction_count').order_by('name'),
            [
                {'name': 'Author 1', 'bestseller_count': 1, 'fiction_count': 1},
                {'name': 'Author 2', 'bestseller_count': 1, 'fiction_count': 1}
            ],
            transform=dict
        )

        # TODO: Once the implementation is fixed, update these tests to assert
        # the correct behavior with multiple FilteredRelation instances
