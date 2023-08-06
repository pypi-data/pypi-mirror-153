from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from wagtail_rest_pack.exception.handler import custom_exception_handler
from wagtail_rest_pack.recaptcha.permission import AuthenticatedOrRecaptcha
from wagtail_rest_pack.comments.content_type import create_content_type_id
from wagtail_rest_pack.comments.models import Comment
from django.utils.translation import gettext as _


class CreateCommentSerializer(ModelSerializer):
    body = serializers.CharField(max_length=2000, required=True)
    content_type = serializers.CharField(max_length=100)
    object_id = serializers.IntegerField()
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), source='parent', required=False)

    class Meta:
        model= Comment
        fields = ['id', 'parent_id', 'body', 'object_id', 'content_type']

    def create(self, validated_data):
        content_type = validated_data.pop('content_type')
        validated_data['content_type_id'] = create_content_type_id(validated_data['object_id'], content_type)
        parent = getattr(validated_data, 'parent', None)
        if parent is not None:
            raise ValidationError(_('Only one level comment tree is supported.'))
        user = self.context['request'].user
        if not user.is_anonymous:
            validated_data['created_by'] = user
        return super(CreateCommentSerializer, self).create(validated_data)


class CreateCommentAPIView(generics.CreateAPIView):
    permission_classes = [AuthenticatedOrRecaptcha]
    serializer_class = CreateCommentSerializer

    def get_exception_handler(self):
        return custom_exception_handler

