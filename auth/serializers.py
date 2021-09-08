from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ExtendUserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = User.get_fields()


class ExtendSignUpSerializer(serializers.Serializer):
    pass
