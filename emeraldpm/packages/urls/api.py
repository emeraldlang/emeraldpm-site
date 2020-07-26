from django.contrib.auth import views as auth_views
from django.urls import path

from .. import views


app_name = 'packages'

urlpatterns = [
    path('download/<str:name>/<str:version>/', views.DownloadVersionAPIView.as_view(), name='download'),
    path('publish/', views.PublishVersionAPIView.as_view(), name='publish'),
    path('package/<str:name>/', views.PackageDetailAPIView.as_view(), name='package'),
    path('package/<str:name>/<str:version>/', views.VersionDetailAPIView.as_view(), name='package'),
]
