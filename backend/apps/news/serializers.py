from rest_framework import serializers

from .models import News
from apps.accounts.models import User
from apps.accounts.serializers import UserReadSerializer
from apps.crossuser.models import UserId

from apps.images.serializers import ImageNewsSerializer, CoverNewsSerializer


class NewsSerializer(serializers.ModelSerializer):

    images_news = ImageNewsSerializer(many=True, read_only=True)
    cover_news = CoverNewsSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(queryset=UserId.objects.all(), slug_field='id_user')
    author_update = serializers.SlugRelatedField(queryset=UserId.objects.all(), slug_field='id_user')
    
    class Meta:
        model = News
        fields = (
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'publicated_at',
            'author',
            'author_update',
            'show_author',
            'images_news',
            'cover_news',
            'slug'
        )

        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class NewsReadSerializer(serializers.ModelSerializer):

    images_news = ImageNewsSerializer(many=True, read_only=True)
    cover_news = CoverNewsSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()
    author_update = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = (
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'publicated_at',
            'author',
            'author_update',
            'show_author',
            'images_news',
            'cover_news',
            'slug'
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


class NewsforCarouselSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = (
            'id',
            'title',
            'slug',
        )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
