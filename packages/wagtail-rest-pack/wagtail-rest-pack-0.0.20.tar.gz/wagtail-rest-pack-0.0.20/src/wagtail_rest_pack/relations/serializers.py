from wagtail.api.v2.serializers import Field


class RelationStreamFieldSerializer(Field):
    def to_representation(self, value):
        return str(value.raw_data)