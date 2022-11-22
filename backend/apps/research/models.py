from django.db import models

from django_extensions.db.fields import AutoSlugField

from apps.crossuser.models import UserId


class ResearchField(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserId, related_name="author_research", on_delete=models.SET_NULL, null=True)
    author_update = models.ForeignKey(UserId, related_name="author_research_update", on_delete=models.SET_NULL, null=True)
    slug = AutoSlugField(populate_from=['title'])
    position = models.IntegerField(default=1)
    show_in_page = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
