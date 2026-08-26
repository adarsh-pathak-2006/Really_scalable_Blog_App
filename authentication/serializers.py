from rest_framework.serializers import ModelSerializer
from ..core.models import Profile
from django.contrib.auth.models import User

class UserGetSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email']

class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'first_name', 'last_name', 'password']

class ProfileGetSerializer(ModelSerializer):
    user=UserGetSerializer(read_only=True)
    class Meta:
        model=Profile
        fields=['user', 'name', 'created_on']

class ProfileSerializer(ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'
        read_only_fields=['user', 'created_on']