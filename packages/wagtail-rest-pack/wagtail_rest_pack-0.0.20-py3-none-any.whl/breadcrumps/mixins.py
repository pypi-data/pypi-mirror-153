
from django.db import models
from wagtail.api import APIField

from breadcrumps.serializers import BreadcrumpSerializer


class BreadcrumpPageMixin(models.Model):

    api_fields= [
        APIField('breadcrumps', BreadcrumpSerializer())
    ]

    @property
    def breadcrumps(self):
        return self

    class Meta:
        abstract= True
