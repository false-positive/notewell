from django.contrib.auth.models import User
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from notes.models import Category, Note
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


class MyStringRelatedField(serializers.StringRelatedField):

    def to_representation(self, value):
        # NOTE: if return value is changed,
        # to_interval_value must be changed
        # in order to match category name
        return value.name.capitalize()

    def to_internal_value(self, data):
        try:
            return get_object_or_404(Category, name__iexact=data)
        except Http404:
            return


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(required=False)
    categories = MyStringRelatedField(
        many=True, allow_null=True, required=False)

    class Meta:
        model = Note
        fields = ('uuid', 'title', 'categories', 'author', 'creation_date')


class NoteViewSerializer(NoteSerializer):
    categories = MyStringRelatedField(many=True)
    author = serializers.StringRelatedField()


class NotePatchSerializer(NoteSerializer):
    # XXX: maybe override get_fields to make it not require subclassing
    # See: https://stackoverflow.com/questions/53735960/
    # (slug ommited from url to make line shorter)
    title = serializers.CharField(required=False)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'full_path', 'children')

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['children'] = CategorySerializer(many=True)
        return fields
