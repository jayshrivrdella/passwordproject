from rest_framework import serializers
from .models import Users


class PwdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'hashvalue']


# class CustomSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length = 100)
#     hashvalue = serializers.CharField(max_length = 100)


class LoginCustomSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    hashvalue = serializers.CharField(max_length=100)


