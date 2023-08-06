
from django.urls import path

from .post import PostFormView

urlpatterns = [
    path('', PostFormView.as_view(), name='form_view'),
]
