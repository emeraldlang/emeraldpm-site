"""emeraldpm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('api/accounts/', include('emeraldpm.accounts.urls.api', namespace='accounts_api')),
    path('', include('emeraldpm.accounts.urls.web', namespace='accounts_web')),

    path('api/packages/', include('emeraldpm.packages.urls.api', namespace='packages_api')),
    path('', include('emeraldpm.packages.urls.web', namespace='packages_web')),

    path('', include('emeraldpm.web.urls', namespace='web')),

    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
