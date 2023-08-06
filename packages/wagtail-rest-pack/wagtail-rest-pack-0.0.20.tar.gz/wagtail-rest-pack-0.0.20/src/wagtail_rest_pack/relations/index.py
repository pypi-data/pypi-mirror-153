import re

from wagtail_rest_pack.relations.models import Relation

page_id_pattern = re.compile('id="([0-9]+)" linktype="page"')


def indexUpdated(**kwargs):
    instance = kwargs['instance']
    if not instance.has_unpublished_changes:
        ids = []
        if hasattr(instance, 'relation_fields'):
            # todo use texteditor handlers if possible
            for field in instance.relation_fields:
                value = field.serializer.to_representation(getattr(instance, field.name))
                ids.extend(page_id_pattern.findall(value))
        relations = []
        for id in set(ids):
            relation = Relation()
            relation.from_page = instance
            relation.to_page_id = id
            relations.append(relation)
        Relation.objects.filter(from_page_id=instance.id).delete()
        for relation in relations:
            relation.save()


def indexDeleted(**kwargs):
    instance = kwargs['instance']
    Relation.objects.filter(to_page_id=instance.id).delete()
    Relation.objects.filter(from_page_id=instance.id).delete()
