from rest_framework import serializers

from .models import Tool
from apps.accounts.models import User
from apps.accounts.serializers import UserReadSerializer
from apps.crossuser.models import UserId

from apps.images.serializers import CoverToolSerializer


class ToolSerializer(serializers.ModelSerializer):

    cover_tool = CoverToolSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(queryset=UserId.objects.all(), slug_field='id_user')
    author_update = serializers.SlugRelatedField(queryset=UserId.objects.all(), slug_field='id_user')
    
    class Meta:
        model = Tool
        fields = (
            'id',
            'name',
            'content',
            'link',
            'created_at',
            'updated_at',
            'author',
            'author_update',
            'show_tool',
            'cover_tool',
            'slug',
        )
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }



class ToolReadSerializer(serializers.ModelSerializer):

    cover_tool = CoverToolSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()
    author_update = serializers.SerializerMethodField()

    class Meta:
        model = Tool
        fields = (
            'id',
            'name',
            'content',
            'link',
            'created_at',
            'updated_at',
            'author',
            'author_update',
            'show_tool',
            'cover_tool',
            'slug',
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
