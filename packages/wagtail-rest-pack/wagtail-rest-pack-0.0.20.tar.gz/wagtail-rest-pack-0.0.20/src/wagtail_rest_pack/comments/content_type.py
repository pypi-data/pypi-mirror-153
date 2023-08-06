from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from wagtail.api.v2.utils import BadRequestError
from django.utils.translation import gettext as _


def create_content_type_id(object_id: str, content_type:str):
    if object_id is None:
        raise BadRequestError(_('`object_id` is not valid'))
    if content_type not in getattr(settings, 'ALLOWED_COMMENTED_CONTENT_TYPES', []):
        raise BadRequestError(_('Given content_type is not allowed to be commented.'))
    if content_type is None or not isinstance(content_type,str):
        raise BadRequestError(_('both content_type and object_id must be supplied.'))
    splitted = content_type.lower().split('.')
    if len(splitted) > 2:
        raise BadRequestError(_('Invalid content_type.'))
    app_label, model = splitted
    content_type_obj = ContentType.objects.get(app_label=app_label,model=model)
    try:
        content_type_obj.get_object_for_this_type(id=int(object_id))
    except content_type_obj.model_class().DoesNotExist:
        raise BadRequestError(_('Given combination of content_type and object_id does not exist'))
    return ContentType.objects.values_list('id').get(app_label=app_label,model=model)[0]
