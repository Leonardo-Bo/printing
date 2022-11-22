from django.db import models

from django_extensions.db.fields import AutoSlugField

from apps.crossuser.models import UserId


class Person(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    github = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    link_scholar = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserId, related_name="author_person", on_delete=models.SET_NULL, null=True)
    author_update = models.ForeignKey(UserId, related_name="author_person_update", on_delete=models.SET_NULL, null=True)
    slug = AutoSlugField(populate_from=['name'])
    position = models.IntegerField(default=1)
    show_in_page = models.BooleanField(default=True)

    def __str__(self):
        return self.name
