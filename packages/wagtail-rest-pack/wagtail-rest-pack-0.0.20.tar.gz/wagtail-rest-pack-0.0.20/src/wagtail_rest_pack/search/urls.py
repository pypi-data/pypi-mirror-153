
from django.urls import path

from .view import SearchView

urlpatterns = [
    path('', SearchView.as_view(), name='search_view'),
]



