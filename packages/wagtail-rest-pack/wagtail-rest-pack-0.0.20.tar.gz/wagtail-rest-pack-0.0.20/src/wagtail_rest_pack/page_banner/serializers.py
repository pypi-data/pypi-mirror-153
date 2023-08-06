from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer
from wagtail.core.models import Page
from wagtail.images.api.fields import ImageRenditionField
from wagtail_rest_pack.streamfield.serializers import SettingsStreamFieldSerializer


class BannerSerializer(serializers.Serializer):
    spec = getattr(settings, 'IMAGE_BANNER_RENDERITION', 'fill-300x200')
    title = serializers.CharField(source='banner_title', required=False)
    subtitle = serializers.CharField(source='banner_subtitle', required=False)
    image = ImageRenditionField(spec, source='banner_image')
    class Meta:
        fields = ['title', 'subtitle', 'image',]

class ChildPageBannerSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.child_extra = kwargs.pop('child_extra', [])
        super(ChildPageBannerSerializer, self).__init__(*args,**kwargs)

    extra = serializers.SerializerMethodField('create_extra')
    banner = BannerSerializer(source='*')
    keywords = serializers.StringRelatedField(many=True)
    class Meta:
        model= Page
        fields=['id', 'slug', 'url', 'last_published_at', 'banner', 'keywords', 'extra']

    def create_extra(self, instance):
        ret = {}
        if 'stream' in self.child_extra:
            ret['stream'] = SettingsStreamFieldSerializer().to_representation(instance.stream)
        return ret

class BanneredChildrenSerializer(Field):

    def to_representation(self, value):
        request = self.context['request']
        order = request.query_params.get('order', '-last_published_at')
        child_extra = request.query_params.get('child_extra', '').split(',')
        qs = value
        if hasattr(value, 'specific'):
            qs = qs.specific()
        if order is not None and hasattr(qs, 'order_by'):
            qs = qs.order_by(order)
        qs = self.context['view'].paginate_queryset(qs)
        return ChildPageBannerSerializer(qs, child_extra=child_extra, many=True).data
