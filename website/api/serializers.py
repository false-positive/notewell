from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class AuthUserTokenObtainPairSerializer(TokenObtainPairSerializer):

    @property
    def data(self):
        data = super().data
        data['user'] = UserSerializer(self.user).data
        return data
