from django.db import models

from django_extensions.db.fields import AutoSlugField

from apps.crossuser.models import UserId


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publicated_at = models.DateField()
    author = models.ForeignKey(UserId, related_name="author_news", on_delete=models.SET_NULL, null=True)
    author_update = models.ForeignKey(UserId, related_name="author_news_update", on_delete=models.SET_NULL, null=True)
    show_author = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from=['title'])
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
