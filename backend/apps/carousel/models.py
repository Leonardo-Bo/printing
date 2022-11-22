from django.db import models

from apps.crossuser.models import UserId
from apps.research.models import ResearchField
from apps.news.models import News


class Carousel(models.Model):
    content = models.CharField(max_length=100, blank=True, null=True)
    field = models.ForeignKey(ResearchField, related_name="carousel_field", on_delete=models.SET_NULL, null=True, blank=True)
    news = models.ForeignKey(News, related_name="carousel_news", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserId, related_name="author_carousel", on_delete=models.SET_NULL, null=True)
    author_update = models.ForeignKey(UserId, related_name="author_carousel_update", on_delete=models.SET_NULL, null=True)
    show_in_home = models.BooleanField(default=True)


    class Meta:
        verbose_name = "Carousel"
        verbose_name_plural = "Carousel"
