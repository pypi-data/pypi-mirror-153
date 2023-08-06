from django.db import models
from wagtail.core.models import Page


class RelationField:
    def __init__(self, name, serializer=None):
        self.name = name
        self.serializer = serializer

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '<APIField {}>'.format(self.name)


class Relation(models.Model):
    from_page = models.ForeignKey(Page, related_name='from_page', on_delete=models.CASCADE)
    to_page = models.ForeignKey(Page, related_name='to_page', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('from_page', 'to_page')
