from django.db import models

from apps.publications.models import Publication
from apps.people.models import Person


def pdf_publication_upload_to(instance, filename):
    return "website/publications/{}/files/{}".format(instance.reffield.pk, filename)


def pdf_person_cv_upload_to(instance, filename):
    return "website/people/{}/files/{}".format(instance.reffield.pk, filename)


class PublicationPDF(models.Model):
    reffield = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='pdf_publication')
    file = models.FileField(upload_to=pdf_publication_upload_to)
    isPDF = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Publication PDF"
        verbose_name_plural = "Publication PDF"


# people

class PersonCVPDF(models.Model):
    reffield = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='pdf_personCV')
    file = models.FileField(upload_to=pdf_person_cv_upload_to)
    isPDF = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
    
    class Meta:
        verbose_name = "Person CV PDF"
        verbose_name_plural = "Person CV PDF"
