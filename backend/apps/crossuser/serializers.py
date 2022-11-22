from rest_framework import serializers
from .models import UserId


class UserIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserId
        fields = (
            "id", 
            "id_user"
        )
