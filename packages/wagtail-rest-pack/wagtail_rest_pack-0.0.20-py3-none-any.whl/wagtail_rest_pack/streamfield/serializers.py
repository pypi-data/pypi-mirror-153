from wagtail.api.v2.serializers import Field
from importlib import import_module
from django.conf import settings


class StreamFieldSerializer(Field):
    def __init__(self, *args, **kwargs):
        self.serializers_instances = kwargs.pop('serializers', {})
        super(StreamFieldSerializer, self).__init__(*args, **kwargs)

    def get_serializers(self):
        return {}

    def all_serializers(self):
        return {**self.get_serializers(), **self.serializers_instances}

    def to_representation(self, value):
        representation = []
        if value is None:
            return representation
        serializers = self.all_serializers()
        for child in value:
            if child.block.name not in serializers.keys():
                child_representation = child.block.get_api_representation(child.value, context=self.context)
            else:
                ser = serializers[child.block.name](context=self.context)
                child_representation = ser.to_representation(child.value)
            representation.append({
                'type': child.block.name,
                'value': child_representation,
                'id': child.id
            })
        return representation


cached = None


def get_stream_field_serializers():
    global cached
    if cached is not None:
        return cached
    resp_pack = getattr(settings, "REST_PACK", {})
    additional_serializers = resp_pack.get('stream_serializers', {})
    form_serializers = {
        'form_text': 'wagtail_rest_pack.generic_forms.blocks.text_block.InputBlockSerializer',
        'form_group': 'wagtail_rest_pack.generic_forms.blocks.group_block.GroupBlockSerializer',
        'form_submit': 'wagtail_rest_pack.generic_forms.blocks.submit_block.SubmitBlockSerializer',
        'form_open_dialog': 'wagtail_rest_pack.generic_forms.blocks.submit_block.OpenDialogSerializer',
        'form': 'wagtail_rest_pack.generic_forms.view.GetFormBuilderSerializer',
        'richtext': 'wagtail_rest_pack.streamfield.richtext.RichTextSerializer',
        'pagelist': 'wagtail_rest_pack.streamfield.page_list.PageListSerializer',
        'container': 'wagtail_rest_pack.streamfield.container.ContainerSerializer',
        'containers': 'wagtail_rest_pack.streamfield.containers.ContainersSerializer',
        'gallery': 'wagtail_rest_pack.streamfield.gallery.GallerySerializer',
        'embedded': 'wagtail_rest_pack.streamfield.embedded.EmbeddedSerializer',
        'gallery_image': 'wagtail_rest_pack.streamfield.image.GalleryImageSerializer',
        'linkblock': 'wagtail_rest_pack.custom_menu.serializers.LinkBlockSerializer',
        'nestedlinkblock': 'wagtail_rest_pack.custom_menu.serializers.LinkBlockSerializer',
        'linkcategory': 'wagtail_rest_pack.custom_menu.serializers.LinkCategorySerializer',
        'categorychildren': 'wagtail_rest_pack.custom_menu.serializers.ChildrenLinksSerializer',
    }
    serializers = {**form_serializers, **additional_serializers}
    classes = {}
    for key, value in serializers.items():
        try:
            module_path, class_name = value.rsplit('.', 1)
            module = import_module(module_path)
            classes[key] = getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            raise ImportError(value)
    cached = classes
    return classes


class SettingsStreamFieldSerializer(StreamFieldSerializer):
    def get_serializers(self):
        return get_stream_field_serializers()
