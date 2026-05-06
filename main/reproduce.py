import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from main.models import ArticleForm

# Simulate form submission
form = ArticleForm(data={})
if form.is_valid():
    article = form.save(commit=False)
    article.save()  # Save the article instance before accessing the many-to-many relationship
    print(article.publications.all())  # This should print an empty queryset
else:
    print("Form is not valid")
