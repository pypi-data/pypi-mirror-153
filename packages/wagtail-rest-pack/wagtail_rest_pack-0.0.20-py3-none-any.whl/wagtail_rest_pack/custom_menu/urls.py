from django.urls import path

from .view import CustomMenuRetrieveSet

urlpatterns = [
    path('<str:name>', CustomMenuRetrieveSet.as_view(), name='custom_menu'),
]