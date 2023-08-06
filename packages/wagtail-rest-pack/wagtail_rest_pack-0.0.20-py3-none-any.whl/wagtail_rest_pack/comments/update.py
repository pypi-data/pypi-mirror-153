import datetime

from rest_framework import generics, serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated

from wagtail_rest_pack.comments.models import Comment
from wagtail_rest_pack.comments.permission import CommentOwnerOrStaff

from wagtail_rest_pack.exception.handler import custom_exception_handler


class UpdateCommentSerializer(ModelSerializer):
    body = serializers.CharField(max_length=2000, required=True)

    class Meta:
        model = Comment
        fields = ['id', 'body']

    def update(self, instance, validated_data):
        validated_data['updated_on'] = datetime.datetime.now()
        validated_data['updated_by'] = self.context['request'].user
        return super(UpdateCommentSerializer, self).update(instance, validated_data)

class DeleteUpdateCommentAPIView(generics.DestroyAPIView, generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, CommentOwnerOrStaff]
    serializer_class = UpdateCommentSerializer
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        return Comment.objects.all()

    def get_exception_handler(self):
        return custom_exception_handler
