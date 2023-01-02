from django.db import models

from apps.crossuser.models import UserId
from apps.research.models import ResearchField


class Publication(models.Model):
    title = models.TextField(unique=True)
    authors = models.TextField()
    magazine = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    doi = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    bibtex = models.TextField(blank=True, null=True)
    corresponding = models.CharField(max_length=255, blank=True, null=True)
    field = models.ManyToManyField(ResearchField, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserId, related_name="author_publication", on_delete=models.SET_NULL, null=True)
    author_update = models.ForeignKey(UserId, related_name="author_publication_update", on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title
