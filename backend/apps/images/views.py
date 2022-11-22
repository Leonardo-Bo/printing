from django.shortcuts import render

from rest_framework import viewsets
import json
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly

from .models import (ImageResearchField, CoverResearchField, 
                     ImagePerson, CoverPerson, PicProfilePerson, 
                     ImageNews, CoverNews, 
                     CoverCarousel, 
                     CoverTool)

from .serializers import (ImageResearchFieldSerializer, CoverResearchFieldSerializer, 
                          ImagePersonSerializer, CoverPersonSerializer, PicProfilePersonSerializer, 
                          ImageNewsSerializer, CoverNewsSerializer,
                          CoverCarouselSerializer, 
                          CoverToolSerializer)


# research 

class ImageResearchFieldViewSet(viewsets.ModelViewSet):
    serializer_class = ImageResearchFieldSerializer
    queryset = ImageResearchField.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = ImageResearchFieldSerializer(data=request.data)
        # print(file_serializer)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoverResearchFieldViewSet(viewsets.ModelViewSet):
    serializer_class = CoverResearchFieldSerializer
    queryset = CoverResearchField.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = CoverResearchFieldSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'isCover' not in request.data:
            file_serializer = CoverResearchFieldSerializer(instance=instance, data={ 'isCover': False }, partial=True)
        else:
            file_serializer = CoverResearchFieldSerializer(instance=instance, data={'isCover': request.data['isCover']}, partial=True)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# people

class ImagePersonViewSet(viewsets.ModelViewSet):
    serializer_class = ImagePersonSerializer
    queryset = ImagePerson.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = ImagePersonSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoverPersonViewSet(viewsets.ModelViewSet):
    serializer_class = CoverPersonSerializer
    queryset = CoverPerson.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = CoverPersonSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'isCover' not in request.data:
            file_serializer = CoverPersonSerializer(instance=instance, data={ 'isCover': False }, partial=True)
        else:
            file_serializer = CoverPersonSerializer(instance=instance, data={'isCover': request.data['isCover']}, partial=True)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PicProfilePersonViewSet(viewsets.ModelViewSet):
    serializer_class = PicProfilePersonSerializer
    queryset = PicProfilePerson.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = PicProfilePersonSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'isPic' not in request.data:
            file_serializer = PicProfilePersonSerializer(instance=instance, data={ 'isPic': False }, partial=True)
        else:
            file_serializer = PicProfilePersonSerializer(instance=instance, data={'isPic': request.data['isPic']}, partial=True)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# news 

class ImageNewsViewSet(viewsets.ModelViewSet):
    serializer_class = ImageNewsSerializer
    queryset = ImageNews.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = ImageNewsSerializer(data=request.data)
        # print(file_serializer)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoverNewsViewSet(viewsets.ModelViewSet):
    serializer_class = CoverNewsSerializer
    queryset = CoverNews.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = CoverNewsSerializer(data=request.data)
        # print(file_serializer)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'isCover' not in request.data:
            file_serializer = CoverNewsSerializer(instance=instance, data={ 'isCover': False }, partial=True)
        else:
            file_serializer = CoverNewsSerializer(instance=instance, data={'isCover': request.data['isCover']}, partial=True)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# carousel

class CoverCarouselViewSet(viewsets.ModelViewSet):
    serializer_class = CoverCarouselSerializer
    queryset = CoverCarousel.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = CoverCarouselSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'isCover' not in request.data:
            file_serializer = CoverCarouselSerializer(instance=instance, data={ 'isCover': False }, partial=True)
        else:
            file_serializer = CoverCarouselSerializer(instance=instance, data={'isCover': request.data['isCover']}, partial=True)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# tools

class CoverToolViewSet(viewsets.ModelViewSet):
    serializer_class = CoverToolSerializer
    queryset = CoverTool.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = CoverToolSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'isCover' not in request.data:
            file_serializer = CoverToolSerializer(instance=instance, data={ 'isCover': False }, partial=True)
        else:
            file_serializer = CoverToolSerializer(instance=instance, data={'isCover': request.data['isCover']}, partial=True)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)