from rest_framework import generics
from wagtail.core.models import Page
from wagtail.search.utils import parse_query_string
from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponse
import json

from wagtail_rest_pack.custom_tag.models import PageTag
from wagtail_rest_pack.page_banner.serializers import BanneredChildrenSerializer
from wagtail.images import get_image_model
import time

from wagtail_rest_pack.streamfield.image import GalleryImageSerializer


class SearchView(generics.RetrieveAPIView):
    def get_serializer_class(self):
        return BanneredChildrenSerializer

    def get_pages_queryset(self):
        return Page.objects.live().public()

    def get_image_queryset(self):
        return get_image_model().objects.all()

    def measure(self, t0):
        return round(time.time() - t0, 3)

    def get(self, request, *args, **kwargs):
        query_string = request.GET.get('q')
        if query_string is None:
            return HttpResponseBadRequest()
        filters, query = parse_query_string(query_string)
        type = filters.get('type')
        if type not in ['pages', 'images', 'documents', 'tags']:
            return HttpResponseBadRequest()
        t0 = time.time()
        if type == 'pages':
            pages = self.get_pages_queryset().specific().search(query)
            pages = self.paginate_queryset(pages)
            ser = BanneredChildrenSerializer()
            ser._context = self.get_serializer_context()
            result = {
                'pages': ser.to_representation(pages),
                'time': self.measure(t0)
            }
        if type == 'images':
            images = self.get_image_queryset().values('id').search(query)
            images = self.paginate_queryset(images)
            result = {
                'images': GalleryImageSerializer(many=True).to_representation(images),
                'time': self.measure(t0)
            }
        if type == 'documents':
            documents = []
            result = {
                'documents': documents,
                'time': self.measure(t0)
            }
        if type == 'tags':
            tags = set(query.query_string.split(' '))
            pages = Page.objects.live().public().filter(id__in=PageTag.objects.filter(tag__name__in=tags).values_list('content_object')).specific()
            pages = self.paginate_queryset(pages)
            ser = BanneredChildrenSerializer()
            ser._context = self.get_serializer_context()
            result = {
                'tags': ser.to_representation(pages),
                'time': self.measure(t0)
            }
        return HttpResponse(json.dumps(result), content_type="application/json")