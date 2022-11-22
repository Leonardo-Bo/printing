from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly

from .models import Carousel

from .serializers import CarouselSerializer, CarouselReadSerializer
import shutil


class CarouselViewSet(viewsets.ModelViewSet):
    queryset = Carousel.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return CarouselReadSerializer
        return CarouselSerializer

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()

        dir_path = 'media/website/carousel/' + str(item.pk)
        item.delete()
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))

        return Response({"message": "Item has been deleted"})
