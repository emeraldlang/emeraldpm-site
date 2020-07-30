from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from ..fields import VERSION_REGEX
from .. import views


app_name = 'packages'

urlpatterns = [
    path('search/', views.PackageSearchView.as_view(), name='search'),
    path('package/<str:name>/', views.PackageDetailView.as_view(), name='package'),
    re_path(r'^package/(?P<name>[^/]+)/(?P<version>{0})/$'.format(VERSION_REGEX), views.PackageDetailView.as_view(), name='package'),
]
