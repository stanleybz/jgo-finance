from rest_framework import serializers
from django.contrib.auth.models import User

# For user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)