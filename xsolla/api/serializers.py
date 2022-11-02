from rest_framework.serializers import Serializer
from rest_framework import serializers


class UserSerializer(Serializer):
    id = serializers.IntegerField()
    country = serializers.CharField()
    email = serializers.EmailField()
    ip = serializers.IPAddressField()
    name = serializers.CharField()
    phone = serializers.CharField()


class SettingsSerializer(Serializer):
    merchant_id = serializers.IntegerField()
    project_id = serializers.IntegerField()


class UserCheckSerializer(Serializer):
    notification_type = serializers.CharField()
    settings = SettingsSerializer()
    user = UserSerializer()
