from django.contrib.auth import views as auth_views
from django.urls import path

from .. import views


app_name = 'packages'

urlpatterns = [
    path('search/', views.PackageSearchView.as_view(), name='search'),
    path('package/<str:name>/', views.PackageDetailView.as_view(), name='package'),
    path('package/<str:name>/<str:version>/', views.PackageDetailView.as_view(), name='package'),
]
