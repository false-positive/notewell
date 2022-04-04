from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from notes.models import Category, Note, SharedItem


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


class UsernameField(serializers.RelatedField):

    queryset = User.objects.all()

    def to_representation(self, user):
        return user.username

    def to_internal_value(self, username):
        try:
            return get_object_or_404(self.get_queryset(), username=username)
        except Http404 as err:
            raise serializers.ValidationError({'username': f'User "{username}" not found'}) from err


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(required=False)
    categories = MyStringRelatedField(
        many=True, allow_null=True, required=False)

    class Meta:
        model = Note
        fields = ('uuid', 'title', 'content', 'categories', 'author', 'creation_date')


class NoteViewSerializer(NoteSerializer):
    categories = MyStringRelatedField(many=True)
    author = serializers.StringRelatedField()


class NotePatchSerializer(NoteSerializer):
    # XXX: maybe override get_fields to make it not require subclassing
    # See: https://stackoverflow.com/q/53735960/
    # (slug ommited from url to make line shorter)
    #
    # or.. use an UpdateAPIView that does it for us
    # See: https://www.django-rest-framework.org/api-guide/generic-views/#updateapiview
    # And: https://www.django-rest-framework.org/api-guide/generic-views/#updatemodelmixin
    title = serializers.CharField(required=False)


class SharedItemSerializer(serializers.ModelSerializer):
    user = UsernameField()
    # XXX: figure out why it doesn't just know that it's supposed to be required
    perm_level = serializers.ChoiceField(
        choices=SharedItem.PERM_LEVEL_CHOICES,
        label='Permission Level',
        required=True,
    )

    class Meta:
        model = SharedItem
        fields = ('user', 'perm_level')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'full_path', 'children')

    def get_fields(self):
        fields = super().get_fields()
        fields['children'] = CategorySerializer(many=True)
        return fields