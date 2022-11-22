from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly

from .models import Tool
from .serializers import ToolSerializer, ToolReadSerializer

import shutil


class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return ToolReadSerializer
        return ToolSerializer


    def destroy(self, request, *args, **kwargs):
        tool = self.get_object()

        dir_path = 'media/website/tools/' + str(tool.pk)
        tool.delete()
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))
        
        return Response({"message": "Item has been deleted"})
