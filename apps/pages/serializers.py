from rest_framework import serializers

from drf_extra_fields.geo_fields import PointField
from rest_framework_recursive.fields import RecursiveField

from apps.pages.models import Page, Image, MasterTag, Comment, Tag
from apps.auth_api.serializers import ShortUserSerializer


class CommentTreeSerializer(serializers.HyperlinkedModelSerializer):
    children = RecursiveField(source='children.all', many=True, read_only=True)
    author_avatar = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = 'id', 'body', 'children', 'author_avatar', 'author'

    def get_author_avatar(self, obj):
        return obj.author.avatar_url

    def get_author(self, obj):
        return obj.author.username


class ImageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        exclude = 'file',

    def get_name(self, obj):
        return obj.file.name.split('/')[-1]

    def get_url(self, obj):
        return obj.file.url


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MasterTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterTag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    author_avatar = serializers.SerializerMethodField()
    def get_author_avatar(self, obj):
        return obj.author.avatar_url

    def get_author(self, obj):
        return obj.author.username
    class Meta:
        model = Comment
        fields = '__all__'


class PageBaseSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    tags_info = TagSerializer(source='tags', read_only=True, many=True)
    uploaded_images = ImageSerializer(many=True, read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    position = PointField()

    class Meta:
        model = Page
        fields = '__all__'

    def get_comments(self, obj):
        return []

    def get_author(self, obj):
        return obj.author.username


class PageListSerializer(PageBaseSerializer):
    body = serializers.SerializerMethodField()
    voters = ShortUserSerializer(many=True, read_only=True)
    miniature = serializers.SerializerMethodField()
    author_avatar = serializers.SerializerMethodField()
    last_comments = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = '__all__'

    def get_author_avatar(self, obj):
        return obj.author.avatar_url

    def get_body(self, obj):
        return obj.body[:100]

    def get_miniature(self, obj):
        return obj.images.first().file.url if obj.images.exists() else None

    def get_last_comments(self, obj):
        qs = obj.comments.all()[:2]

        return CommentSerializer(qs, many=True).data


class PageSerializer(PageBaseSerializer):
    class Meta:
        model = Page
        fields = '__all__'
