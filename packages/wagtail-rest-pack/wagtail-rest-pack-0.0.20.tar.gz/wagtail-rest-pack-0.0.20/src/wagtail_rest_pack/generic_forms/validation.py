from wagtail_rest_pack.streamfield.serializers import get_stream_field_serializers


def validate_stream_data(data, stream_data, **kwargs):
    for stream_value in stream_data:
        type = stream_value['type']
        serializer_class = kwargs['serializers'].get(type, None)
        block_value = stream_value['value']
        serializer = serializer_class(context={'instance': block_value, **kwargs})
        if hasattr(serializer, 'validate_field'):
            result = serializer.validate_field(data)
            if result is not None:
                for key, value in result.items():
                    kwargs['validated_data'][key] = value
        if block_value.get('stream',None) is not None:
            stream_data = block_value['stream']
            validate_stream_data(data, stream_data, **kwargs)
    return kwargs['validated_data']

def validate_form_data(data, **kwargs):
    kwargs['serializers'] = get_stream_field_serializers()
    kwargs['validated_data'] = {}
    return validate_stream_data(data, kwargs['form'].stream.stream_data, **kwargs)

