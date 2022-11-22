from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly

from .models import Person

from .serializers import PersonSerializer, PersonReadSerializer
import shutil


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    # serializers = PersonSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return PersonReadSerializer
        return PersonSerializer

    def destroy(self, request, *args, **kwargs):
        person = self.get_object()

        dir_path = 'media/website/people/' + str(person.pk)
        person.delete()
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))

        return Response({"message": "Item has been deleted"})
