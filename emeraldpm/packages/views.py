from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Package


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
