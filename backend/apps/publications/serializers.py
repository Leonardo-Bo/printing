from rest_framework import serializers

from .models import Publication
from apps.accounts.models import User
from apps.accounts.serializers import UserReadSerializer
from apps.crossuser.models import UserId
from apps.research.serializers import ResearchFieldforPublicationSerializer

from apps.files.serializers import PublicationPDFSerializer


class PublicationSerializer(serializers.ModelSerializer):

    pdf_publication = PublicationPDFSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(queryset=UserId.objects.all(), slug_field='id_user')
    author_update = serializers.SlugRelatedField(queryset=UserId.objects.all(), slug_field='id_user')
    
    class Meta:
        model = Publication
        fields = (
            'id',
            'title',
            'authors',
            'magazine',
            'year',
            'doi',
            'link',
            'bibtex',
            'corresponding',
            'field',
            'created_at',
            'updated_at',
            'author',
            'author_update',
            'pdf_publication',
        )


class PublicationReadSerializer(serializers.ModelSerializer):

    pdf_publication = PublicationPDFSerializer(many=True, read_only=True)
    field = ResearchFieldforPublicationSerializer(many=True)
    author = serializers.SerializerMethodField()
    author_update = serializers.SerializerMethodField()
    
    class Meta:
        model = Publication
        fields = (
            'id',
            'title',
            'authors',
            'magazine',
            'year',
            'doi',
            'link',
            'bibtex',
            'corresponding',
            'field',
            'created_at',
            'updated_at',
            'author',
            'author_update',
            'pdf_publication',
        )

    def get_author(self, obj):
        author = User.objects.filter(id=obj.author.id_user)
        return UserReadSerializer(author, many=True).data

    def get_author_update(self, obj):
        author_update = User.objects.filter(id=obj.author_update.id_user)
        return UserReadSerializer(author_update, many=True).data
