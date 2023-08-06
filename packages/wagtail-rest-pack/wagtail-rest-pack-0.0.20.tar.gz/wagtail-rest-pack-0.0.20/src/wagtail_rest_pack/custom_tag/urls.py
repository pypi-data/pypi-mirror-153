from django.urls import path

from .view import TagViewset

urlpatterns = [
    path('', TagViewset.as_view(), name='tags_view'),
]