import django
from django.conf import settings
from django.db import models
from django import forms
from django.core.management import call_command
settings.configure(
    INSTALLED_APPS=[
        'myapp.apps.MyAppConfig',
    ],
    MIDDLEWARE=[],
    ROOT_URLCONF='myapp.urls',
    TEMPLATES=[],
    TIME_ZONE='UTC',
    USE_TZ=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
)
django.setup()
call_command('makemigrations', 'myapp')
call_command('migrate')
django.setup()
call_command('makemigrations', 'myapp')
call_command('migrate')
class ArticleManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(archived=False)

class Article(models.Model):
    title = models.CharField(max_length=100)
    archived = models.BooleanField(default=False)
    objects = ArticleManager()

    class Meta:
        app_label = 'myapp'

class FavoriteArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        app_label = 'myapp'
class FavoriteArticleForm(forms.ModelForm):
    class Meta:
        model = FavoriteArticle
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['article'].queryset = Article._base_manager.all()

# Create an archived article
archived_article = Article.objects.create(title="Archived Article", archived=True)

# Create a form instance with the archived article
form = FavoriteArticleForm(data={'article': archived_article.id})

# Check if the form is valid
print("Is the form valid?", form.is_valid())
print("Form errors:", form.errors)
