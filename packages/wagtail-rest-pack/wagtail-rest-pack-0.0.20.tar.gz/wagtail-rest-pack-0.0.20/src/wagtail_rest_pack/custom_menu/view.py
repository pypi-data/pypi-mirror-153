from rest_framework import generics
from rest_framework import serializers
from wagtail_rest_pack.streamfield.serializers import SettingsStreamFieldSerializer

from .models import CustomMenu


class CustomMenuSerializer(serializers.ModelSerializer):
    stream = SettingsStreamFieldSerializer()
    class Meta:
        model = CustomMenu
        fields = ['name', 'stream',]


class CustomMenuRetrieveSet(generics.RetrieveAPIView):
    model = CustomMenu
    lookup_field = 'name'
    queryset = CustomMenu.objects.all()
    serializer_class = CustomMenuSerializer
