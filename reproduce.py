from django.db.models import Count
from myapp.models import Book

# Reproduce the issue
count_with_annotation = Book.objects.annotate(Count('chapters')).count()
count_without_annotation = Book.objects.count()

print("Count with annotation:", count_with_annotation)
print("Count without annotation:", count_without_annotation)
