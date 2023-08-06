from django.http import HttpResponseNotFound


def local_network_only(view_func):
    def wrapped_view(*args, **kwargs):
        if args[0].headers.get('x-forwarded-for') is None:
            return view_func(*args, **kwargs)
        return HttpResponseNotFound()
    return wrapped_view
