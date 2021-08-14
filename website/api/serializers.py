from notes.models import Category, Note
from rest_framework import serializers


class MyStringRelatedField(serializers.StringRelatedField):

    def to_representation(self, value):
        # TODO not exactly todo, but
        # if join is changed in category model in __str__
        # split argument must match it

        return f'{value.name}'.capitalize()


class NoteSerializer(serializers.ModelSerializer):
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
