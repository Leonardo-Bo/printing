from django.db import models

from django_extensions.db.fields import AutoSlugField

from apps.crossuser.models import UserId


class Tool(models.Model):
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=150, blank=True, null=True)
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserId, related_name="author_tool", on_delete=models.SET_NULL, null=True)
    author_update = models.ForeignKey(UserId, related_name="author_tool_update", on_delete=models.SET_NULL, null=True)
    show_tool = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from=['name'])
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Tool"
        verbose_name_plural = "Tools"
