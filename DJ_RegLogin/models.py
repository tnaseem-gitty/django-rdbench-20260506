from django.db import models
from django.urls import reverse

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    class Meta:
        app_label = 'DJ_RegLogin'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_blog_category', None, kwargs={'slug': self.slug})

class Content(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    sites = models.ManyToManyField('sites.Site')
    ip = models.GenericIPAddressField(editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=False, blank=False, editable=False)
    class Meta:
        app_label = 'DJ_RegLogin'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_blog_post', None, kwargs={'slug': self.slug})
