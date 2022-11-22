from rest_framework import serializers

from .models import (ImageResearchField, CoverResearchField, 
                     ImagePerson, CoverPerson, PicProfilePerson, 
                     ImageNews, CoverNews, 
                     CoverCarousel, 
                     CoverTool)


# research fields

class ImageResearchFieldSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()

    class Meta:
        model = ImageResearchField
        fields = ['id', 'reffield', 'image', 'size']

    def get_size(self, obj):
        image_size = ''
        if obj.image and hasattr(obj.image, 'size'):
            image_size = obj.image.size
        return image_size

    def to_representation(self, instance):
        response = super(ImageResearchFieldSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


class CoverResearchFieldSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()

    class Meta:
        model = CoverResearchField
        fields = ['id', 'reffield', 'image', 'isCover', 'size']

    def get_size(self, obj):
        image_size = ''
        if obj.image and hasattr(obj.image, 'size'):
            image_size = obj.image.size
        return image_size

    def to_representation(self, instance):
        response = super(CoverResearchFieldSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response



# people

class ImagePersonSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()

    class Meta:
        model = ImagePerson
        fields = ['id', 'reffield', 'image', 'size']

    def get_size(self, obj):
        image_size = ''
        if obj.image and hasattr(obj.image, 'size'):
            image_size = obj.image.size
        return image_size

    def to_representation(self, instance):
        response = super(ImagePersonSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


class CoverPersonSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()

    class Meta:
        model = CoverPerson
        fields = ['id', 'reffield', 'image', 'isCover', 'size']

    def get_size(self, obj):
        image_size = ''
        if obj.image and hasattr(obj.image, 'size'):
            image_size = obj.image.size
        return image_size

    def to_representation(self, instance):
        response = super(CoverPersonSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


class PicProfilePersonSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()

    class Meta:
        model = PicProfilePerson
        fields = ['id', 'reffield', 'image', 'isPic', 'size']

    def get_size(self, obj):
        image_size = ''
        if obj.image and hasattr(obj.image, 'size'):
            image_size = obj.image.size
        return image_size

    def to_representation(self, instance):
        response = super(PicProfilePersonSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response



# news

class ImageNewsSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()

    class Meta:
        model = ImageNews
        fields = ['id', 'reffield', 'image', 'size']

    def get_size(self, obj):
        image_size = ''
        if obj.image and hasattr(obj.image, 'size'):
            image_size = obj.image.size
        return image_size

    def to_representation(self, instance):
        response = super(ImageNewsSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


class CoverNewsSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()

    class Meta:
        model = CoverNews
        fields = ['id', 'reffield', 'image', 'isCover', 'size']

    def get_size(self, obj):
        image_size = ''
        if obj.image and hasattr(obj.image, 'size'):
            image_size = obj.image.size
        return image_size

    def to_representation(self, instance):
        response = super(CoverNewsSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


# carousel

class CoverCarouselSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()

    class Meta:
        model = CoverCarousel
        fields = ['id', 'reffield', 'image', 'isCover', 'size']

    def get_size(self, obj):
        image_size = ''
        if obj.image and hasattr(obj.image, 'size'):
            image_size = obj.image.size
        return image_size

    def to_representation(self, instance):
        response = super(CoverCarouselSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


# tools

class CoverToolSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()

    class Meta:
        model = CoverTool
        fields = ['id', 'reffield', 'image', 'isCover', 'size']

    def get_size(self, obj):
        image_size = ''
        if obj.image and hasattr(obj.image, 'size'):
            image_size = obj.image.size
        return image_size

    def to_representation(self, instance):
        response = super(CoverToolSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response
