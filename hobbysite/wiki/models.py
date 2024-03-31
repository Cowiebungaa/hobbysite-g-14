from django.db import models
from django.utils import timezone

class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(ArticleCategory, on_delete=models.SET_NULL, null=True)
    entry = models.TextField()
    created_on = models.DateTimeField(default=timezone.now, editable=False)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title



