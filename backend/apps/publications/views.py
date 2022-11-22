from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly

from .models import Publication

from .serializers import PublicationSerializer, PublicationReadSerializer
import shutil


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return PublicationReadSerializer
        return PublicationSerializer


    def destroy(self, request, *args, **kwargs):
        publication = self.get_object()

        dir_path = 'media/website/publications/' + str(publication.pk)
        publication.delete()
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))

        return Response({"message": "Item has been deleted"})
