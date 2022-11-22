from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly

from .models import ResearchField

from .serializers import ResearchFieldSerializer, ResearchFieldReadSerializer

import shutil


class ResearchFieldViewSet(viewsets.ModelViewSet):
    # serializer_class = ResearchFieldSerializer
    queryset = ResearchField.objects.all()
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ResearchFieldReadSerializer
        return ResearchFieldSerializer


    def destroy(self, request, *args, **kwargs):
        research_field = self.get_object()

        dir_path = 'media/website/research/' + str(research_field.pk)
        research_field.delete()
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))
        
        # return super(ResearchFieldViewSet, self).delete(request, *args, **kwargs)
        return Response({"message": "Item has been deleted"})