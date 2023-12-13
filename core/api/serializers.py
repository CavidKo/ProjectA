from rest_framework import serializers
from core.models import *

class GetBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('name', 'description', 'create_time')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('category',)

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = ('color',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('tag',)

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sizes
        fields = ('size',)

class GetClothesSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    color = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    class Meta:
        model = Clothes
        fields = ('name', 'description', 'price', 'category', 'color', 'tag', 'size', 'weight', 'length', 'width', 'height', 'materials', 'create_time')

    def get_size(self, obj):
        sizes = obj.size.all()
        size_serializer = SizeSerializer(sizes, many=True)
        return size_serializer.data

    def get_tag(self, obj):
        tags = obj.tag.all()
        tag_serializer = TagSerializer(tags, many=True)
        return tag_serializer.data

    def get_color(self, obj):
        colors = obj.color.all()
        color_serializer = ColorSerializer(colors, many=True)
        return color_serializer.data

# class PostBlogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Blog
#         fields = ('name', 'description', 'author', 'categories', 'tags', 'create_time')

# class ChangeWhishSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Clothes
#         fields = ('id', 'name', 'added_to_whishlist')