from django.http import Http404
from rest_framework.response import Response
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.serializers import PageSerializer
from wagtail.core.models import Page
from rest_framework.permissions import AllowAny

class NotRedirectWhenFindViewPagesApiViewSet(PagesAPIViewSet):

    def find_view(self, request):
        queryset = self.get_queryset()
        try:
            obj = self.find_object(queryset, request)
            if obj is None:
                raise self.model.DoesNotExist
        except self.model.DoesNotExist:
            raise Http404("not found")
        self.kwargs['pk'] = obj.pk
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
