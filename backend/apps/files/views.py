from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly

from .models import PublicationPDF, PersonCVPDF
from .serializers import PublicationPDFSerializer, PersonCVPDFSerializer


class PublicationPDFViewSet(viewsets.ModelViewSet):
    serializer_class = PublicationPDFSerializer
    queryset = PublicationPDF.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = PublicationPDFSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'isPDF' not in request.data:
            file_serializer = PublicationPDFSerializer(instance=instance, data={ 'isPDF': False }, partial=True)
        else:
            file_serializer = PublicationPDFSerializer(instance=instance, data={'isPDF': request.data['isPDF']}, partial=True)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonCVPDFViewSet(viewsets.ModelViewSet):
    serializer_class = PersonCVPDFSerializer
    queryset = PersonCVPDF.objects.all()

    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        file_serializer = PersonCVPDFSerializer(data=request.data)
        
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'isPDF' not in request.data:
            file_serializer = PersonCVPDFSerializer(instance=instance, data={ 'isPDF': False }, partial=True)
        else:
            file_serializer = PersonCVPDFSerializer(instance=instance, data={'isPDF': request.data['isPDF']}, partial=True)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
