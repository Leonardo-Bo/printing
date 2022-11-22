from django.db import models

from apps.research.models import ResearchField
from apps.people.models import Person
from apps.news.models import News
from apps.carousel.models import Carousel
from apps.tools.models import Tool


def research_images_upload_to(instance, filename):
    return "website/research/{}/images/{}".format(instance.reffield.pk, filename)

def research_cover_upload_to(instance, filename):
    return "website/research/{}/images/cover/{}".format(instance.reffield.pk, filename)


def person_images_upload_to(instance, filename):
    return "website/people/{}/images/{}".format(instance.reffield.pk, filename)

def person_cover_upload_to(instance, filename):
    return "website/people/{}/images/cover/{}".format(instance.reffield.pk, filename)

def person_pic_upload_to(instance, filename):
    return "website/people/{}/images/profile_pics/{}".format(instance.reffield.pk, filename)


def news_images_upload_to(instance, filename):
    return "website/news/{}/images/{}".format(instance.reffield.pk, filename)

def news_cover_upload_to(instance, filename):
    return "website/news/{}/images/cover/{}".format(instance.reffield.pk, filename)


def carousel_upload_to(instance, filename):
    return "website/carousel/{}/{}".format(instance.reffield.pk, filename)


def tool_upload_to(instance, filename):
    return "website/tools/{}/{}".format(instance.reffield.pk, filename)


# research fields

class ImageResearchField(models.Model):
    reffield = models.ForeignKey(ResearchField, on_delete=models.CASCADE, related_name='images_research')
    image = models.ImageField(upload_to=research_images_upload_to)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class CoverResearchField(models.Model):
    reffield = models.ForeignKey(ResearchField, on_delete=models.CASCADE, related_name='cover_research')
    image = models.ImageField(upload_to=research_cover_upload_to)
    isCover = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)



# people

class ImagePerson(models.Model):
    reffield = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='images_person')
    image = models.ImageField(upload_to=person_images_upload_to)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class CoverPerson(models.Model):
    reffield = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='cover_person')
    image = models.ImageField(upload_to=person_cover_upload_to)
    isCover = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class PicProfilePerson(models.Model):
    reffield = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='pic_person')
    image = models.ImageField(upload_to=person_pic_upload_to)
    isPic = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)



# news

class ImageNews(models.Model):
    reffield = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images_news')
    image = models.ImageField(upload_to=news_images_upload_to)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Image news"
        verbose_name_plural = "Image news"


class CoverNews(models.Model):
    reffield = models.ForeignKey(News, on_delete=models.CASCADE, related_name='cover_news')
    image = models.ImageField(upload_to=news_cover_upload_to)
    isCover = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Cover news"
        verbose_name_plural = "Cover news"


# carousel

class CoverCarousel(models.Model):
    reffield = models.ForeignKey(Carousel, on_delete=models.CASCADE, related_name='cover_carousel')
    image = models.ImageField(upload_to=carousel_upload_to)
    isCover = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


# tools

class CoverTool(models.Model):
    reffield = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='cover_tool')
    image = models.ImageField(upload_to=tool_upload_to)
    isCover = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)