import os
import sys
import django
from django.conf import settings
from django.core.management import call_command

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
django.setup()

from django import forms
from django.contrib import admin
from django.test import TestCase
from test_app.models import Publication, Article

class ArticleForm(forms.ModelForm):
    publications = forms.ModelMultipleChoiceField(
        Publication.objects.filter(id__lt=2).union(
            Publication.objects.filter(id__gt=5)
        ),
        required=False,
    )
    class Meta:
        model = Article
        fields = ["publications"]

    def clean_publications(self):
        publications = self.cleaned_data.get('publications')
        if self.data.get('publications') == []:
            return Publication.objects.none()
        return publications

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        instance.publications.set(self.cleaned_data.get('publications', []))
        return instance

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm

class QuerySetNoneTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not os.path.exists('test_app/migrations'):
            os.makedirs('test_app/migrations')
        if not os.path.exists('test_app/migrations/__init__.py'):
            open('test_app/migrations/__init__.py', 'a').close()
        if not os.path.exists('test_app/migrations/0001_initial.py'):
            with open('test_app/migrations/0001_initial.py', 'w') as f:
                f.write('''
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('publications', models.ManyToManyField(blank=True, to='test_app.Publication')),
            ],
        ),
    ]
''')
        call_command('migrate', 'test_app', interactive=False)

    def setUp(self):
        for i in range(10):
            Publication.objects.create(name=f"Publication {i}")
        self.article = Article.objects.create(title="Test Article")

    def test_queryset_none(self):
        form_data = {'publications': []}
        form = ArticleForm(data=form_data, instance=self.article)
        self.assertTrue(form.is_valid())
        form.save()
        print(f"Publications before save: {list(self.article.publications.all())}")
        print(f"Form cleaned data: {form.cleaned_data}")
        print(f"Publications after save: {list(self.article.publications.all())}")
        self.assertEqual(self.article.publications.count(), 0)

if __name__ == '__main__':
    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["__main__"])
    print("Test failures:", failures)
