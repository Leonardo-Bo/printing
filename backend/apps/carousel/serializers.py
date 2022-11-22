from rest_framework import serializers

from .models import Carousel
from apps.accounts.models import User
from apps.accounts.serializers import UserReadSerializer
from apps.crossuser.models import UserId

from apps.images.serializers import CoverCarouselSerializer

from apps.research.serializers import ResearchFieldforPublicationSerializer
from apps.news.serializers import NewsforCarouselSerializer


class CarouselSerializer(serializers.ModelSerializer):

    cover_carousel = CoverCarouselSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(queryset=UserId.objects.all(), slug_field='id_user')
    author_update = serializers.SlugRelatedField(queryset=UserId.objects.all(), slug_field='id_user')
    
    class Meta:
        model = Carousel
        fields = (
            'id',
            'content',
            'field',
            'news',
            'created_at',
            'updated_at',
            'author',
            'author_update',
            'cover_carousel',
            'show_in_home',
        )


class CarouselReadSerializer(serializers.ModelSerializer):

    cover_carousel = CoverCarouselSerializer(many=True, read_only=True)
    field = ResearchFieldforPublicationSerializer()
    news = NewsforCarouselSerializer()
    author = serializers.SerializerMethodField()
    author_update = serializers.SerializerMethodField()

    class Meta:
        model = Carousel
        fields = (
            'id',
            'content',
            'field',
            'news',
            'created_at',
            'updated_at',
            'author',
            'author_update',
            'cover_carousel',
            'show_in_home',
        )
    
    def get_author(self, obj):
        author = User.objects.filter(id=obj.author.id_user)
        return UserReadSerializer(author, many=True).data

    def get_author_update(self, obj):
        author_update = User.objects.filter(id=obj.author_update.id_user)
        return UserReadSerializer(author_update, many=True).data
