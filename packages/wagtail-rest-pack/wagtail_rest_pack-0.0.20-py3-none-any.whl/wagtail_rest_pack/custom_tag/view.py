from rest_framework import generics
from rest_framework import serializers

from .models import PageTag


class TagSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(source="tag__name")
    class Meta:
        model = PageTag
        fields = ['tag']


class TagViewset(generics.ListAPIView):
    model = PageTag
    queryset = PageTag.objects.values('tag__name').distinct() # todo lists all tags, I need a set, no duplicates plase :)
    serializer_class = TagSerializer
