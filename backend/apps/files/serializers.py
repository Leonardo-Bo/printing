from rest_framework import serializers

from .models import PublicationPDF, PersonCVPDF


class PublicationPDFSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()

    class Meta:
        model = PublicationPDF
        fields = ['id', 'reffield', 'file', 'isPDF', 'size']

    def get_size(self, obj):
        file_size = ''
        if obj.file and hasattr(obj.file, 'size'):
            file_size = obj.file.size
        return file_size

    def to_representation(self, instance):
        response = super(PublicationPDFSerializer, self).to_representation(instance)
        if instance.file:
            response['file'] = instance.file.url
        return response


class PersonCVPDFSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()

    class Meta:
        model = PersonCVPDF
        fields = ['id', 'reffield', 'file', 'isPDF', 'size']

    def get_size(self, obj):
        file_size = ''
        if obj.file and hasattr(obj.file, 'size'):
            file_size = obj.file.size
        return file_size

    def to_representation(self, instance):
        response = super(PersonCVPDFSerializer, self).to_representation(instance)
        if instance.file:
            response['file'] = instance.file.url
        return response
