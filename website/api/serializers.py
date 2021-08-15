from django.contrib.auth.models import User
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from notes.models import Category, Note
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MyStringRelatedField(serializers.StringRelatedField):

    def to_representation(self, value):
        # TODO not exactly todo, but
        # if return value is changed,
        # to_interval_value must be changed
        # in order to match category name
        return f'{value.name}'.capitalize()

    def to_internal_value(self, data):
        try:
            return get_object_or_404(Category, name__iexact=data)
        except Http404:
            return


class NoteSerializer(serializers.ModelSerializer):
    categories = MyStringRelatedField(
        many=True, allow_null=True, required=False)

    class Meta:
        model = Note
        fields = ('title', 'categories')


class ViewNoteSerializer(serializers.ModelSerializer):
    title = serializers.StringRelatedField()
    categories = MyStringRelatedField(many=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Note
        fields = '__all__'


# class CategorySerializer(serializers.ModelSerializer):
#     parent = serializers.PrimaryKeyRelatedField(read_only=True)

#     class Meta:
#         model = Category
#         fields = ('parent', 'name', 'children')

#         def get_related_field(self, model_field):
#             # Handles initializing the `subcategories` field
#             return CategorySerializer()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'children')

    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields['children'] = CategorySerializer(many=True)
        return fields
