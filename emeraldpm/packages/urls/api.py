from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from ..fields import VERSION_REGEX
from .. import views


app_name = 'packages'

urlpatterns = [
    re_path(r'^download/(?P<name>\w+)/(?P<version>{0})/$'.format(VERSION_REGEX), views.DownloadVersionAPIView.as_view(), name='download'),
    path('publish/', views.PublishVersionAPIView.as_view(), name='publish'),
    path('package/<str:name>/', views.PackageDetailAPIView.as_view(), name='package'),
    re_path(r'^package/(?P<name>\w+)/(?P<version>{0})/$'.format(VERSION_REGEX), views.VersionDetailAPIView.as_view(), name='package'),
]
