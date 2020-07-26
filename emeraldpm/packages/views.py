import datetime
import os

from django.db.models import F
from django.http import FileResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DownloadCount, Package, Version
from .serializers import PackageSerializer, VersionSerializer


class PackageSearchView(ListView):
    template_name = 'packages/search.html'
    context_object_name = 'packages'

    def get_queryset(self):
        if 'q' in self.request.GET:
            return Package.objects.filter(name__icontains=self.request.GET['q'])
        else:
            return Package.objects.all()


class PackageDetailView(DetailView):
    template_name = 'packages/package.html'
    model = Package
    context_object_name = 'package'
    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'version' in self.kwargs:
            context['version'] = self.object.versions.get(version=self.kwargs['version'])
        else:
            context['version'] = self.object.versions.latest()
        return context


class PublishVersionAPIView(CreateAPIView):
    serializer_class = VersionSerializer


class PackageDetailAPIView(RetrieveAPIView):
    serializer_class = PackageSerializer
    queryset = Package.objects.all()
    lookup_field = 'name'


class VersionDetailAPIView(RetrieveAPIView):
    serializer_class = VersionSerializer
    lookup_field = 'version'

    def get_queryset(self):
        return Version.objects.filter(package__name=self.kwargs['name'])


class DownloadVersionAPIView(APIView):
    def get(self, request, name, version):
        version = Version.objects.get(
            package__name=name,
            version=version)
        today = datetime.date.today()
        download_count, _ = DownloadCount.objects.get_or_create(
            package__name=name,
            day=today,
            defaults={
                'package': Package.objects.get(name=name),
                'day': today
            })

        file = version.archive.open()
        res = FileResponse(file, content_type='application/zip')
        res['Content-Length'] = version.archive.size
        res['Content-Disposition'] = 'attachment; filename=%s' % (
            os.path.basename(version.archive.name))

        download_count.count = F('count') + 1
        download_count.save(update_fields=('count',))

        return res
