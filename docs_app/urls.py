from django.urls import path, re_path
from django.views.static import serve
from .views import redirectToIndex

urlpatterns = [
    path('', redirectToIndex),
    re_path(r'^(?P<path>.*)$', serve, {
        'document_root': 'docs_app/docs/_build/html/',
    }),
]