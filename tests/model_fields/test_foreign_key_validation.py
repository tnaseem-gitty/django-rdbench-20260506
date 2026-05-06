from django.db import models
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.forms import ModelForm

class ArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(archived=False)

class Article(models.Model):
    title = models.CharField(max_length=100)
    archived = models.BooleanField(default=False)
    objects = ArticleManager()

class FavoriteArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

class FavoriteArticleForm(ModelForm):
    class Meta:
        model = FavoriteArticle
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['article'].queryset = Article._base_manager.all()

class ForeignKeyValidationTest(TestCase):
    def setUp(self):
        self.archived_article = Article.objects.create(title="Archived Article", archived=True)
        self.active_article = Article.objects.create(title="Active Article", archived=False)

    def test_foreign_key_validation_with_archived_article(self):
        form = FavoriteArticleForm(data={'article': self.archived_article.pk})
        self.assertTrue(form.is_valid())

    def test_foreign_key_validation_with_active_article(self):
        form = FavoriteArticleForm(data={'article': self.active_article.pk})
        self.assertTrue(form.is_valid())

    def test_foreign_key_validation_with_nonexistent_article(self):
        form = FavoriteArticleForm(data={'article': 9999})  # Assuming 9999 is not a valid PK
        self.assertFalse(form.is_valid())
