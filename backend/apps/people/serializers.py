from rest_framework import serializers

from .models import Person
from apps.accounts.models import User
from apps.accounts.serializers import UserReadSerializer
from apps.crossuser.models import UserId

from apps.files.serializers import PersonCVPDFSerializer
from apps.images.serializers import ImagePersonSerializer, CoverPersonSerializer, PicProfilePersonSerializer


class PersonSerializer(serializers.ModelSerializer):

    pdf_personCV = PersonCVPDFSerializer(many=True, read_only=True)
    images_person = ImagePersonSerializer(many=True, read_only=True)
    cover_person = CoverPersonSerializer(many=True, read_only=True)
    pic_person = PicProfilePersonSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(queryset=UserId.objects.all(), slug_field='id_user')
    author_update = serializers.SlugRelatedField(queryset=UserId.objects.all(), slug_field='id_user')
    
    class Meta:
        model = Person
        fields = (
            'id',
            'name',
            'email',
            'role',
            'github',
            'linkedin',
            'content',
            'link_scholar',
            'created_at',
            'updated_at',
            'author',
            'author_update',
            'images_person',
            'cover_person',
            'pic_person',
            'pdf_personCV',
            'slug',
            'position',
            'show_in_page'
        )

        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class PersonReadSerializer(serializers.ModelSerializer):

    pdf_personCV = PersonCVPDFSerializer(many=True, read_only=True)
    images_person = ImagePersonSerializer(many=True, read_only=True)
    cover_person = CoverPersonSerializer(many=True, read_only=True)
    pic_person = PicProfilePersonSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()
    author_update = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        fields = (
            'id',
            'name',
            'email',
            'role',
            'github',
            'linkedin',
            'content',
            'link_scholar',
            'created_at',
            'updated_at',
            'author',
            'author_update',
            'images_person',
            'cover_person',
            'pic_person',
            'pdf_personCV',
            'slug',
            'position',
            'show_in_page'
        )

        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

    def get_author(self, obj):
        author = User.objects.filter(id=obj.author.id_user)
        return UserReadSerializer(author, many=True).data

    def get_author_update(self, obj):
        author_update = User.objects.filter(id=obj.author_update.id_user)
        return UserReadSerializer(author_update, many=True).data
