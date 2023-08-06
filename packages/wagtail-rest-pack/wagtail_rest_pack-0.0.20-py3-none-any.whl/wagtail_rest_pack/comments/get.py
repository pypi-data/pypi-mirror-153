from rest_framework import generics
from rest_framework.fields import SerializerMethodField
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from wagtail.users.models import UserProfile
from wagtail_rest_pack.exception.handler import custom_exception_handler
from django.contrib.auth import get_user_model

from wagtail_rest_pack.comments.content_type import create_content_type_id
from wagtail_rest_pack.comments.models import Comment


class PageAuthorUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['avatar']


class CommentAuthorSerializer(serializers.ModelSerializer):
    profile = PageAuthorUserProfileSerializer(source='wagtail_userprofile', read_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ['is_staff', 'is_superuser', 'username', 'first_name', 'last_name', 'profile']


class GetCommentSerializer(ModelSerializer):
    children = SerializerMethodField('_get_children')
    author = CommentAuthorSerializer(source="created_by")
    updated_by = CommentAuthorSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'parent', 'created_on', 'author', 'updated_on', 'updated_by', 'body', 'children']

    def _get_children(self, obj):
        children = Comment.objects.filter(parent_id=obj.id).order_by('created_on')
        serializer = GetCommentSerializer(children, many=True)
        return serializer.data


class ListCommentAPIView(generics.ListAPIView):
    """
    example: /?content_type=wagtailcore.Page&object_id=4
    """
    permission_classes = [AllowAny]
    serializer_class = GetCommentSerializer

    def get_queryset(self):
        object_id = self.request.query_params.get('object_id', None)
        content_type = self.request.query_params.get('content_type', None)
        content_type_id = create_content_type_id(object_id, content_type)
        return Comment.objects.filter(object_id=object_id, content_type_id=content_type_id, parent=None).order_by('created_on')

    def get_exception_handler(self):
        return custom_exception_handler
