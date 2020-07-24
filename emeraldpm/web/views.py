from datetime import date, timedelta

from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import TemplateView

from emeraldpm.packages.models import Package, DownloadCount, Version


class HomeView(TemplateView):
    template_name = 'web/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_packages'] = Package.objects.count()
        context['downloads_last_week'] = DownloadCount.objects\
            .filter(day__gt=date.today() - timedelta(weeks=1))\
            .aggregate(count=Sum('count'))['count'] or 0
        context['downloads_last_30_days'] = DownloadCount.objects\
            .filter(day__gt=date.today() - timedelta(days=30))\
            .aggregate(count=Sum('count'))['count'] or 0
        context['recently_published'] = Version.objects.order_by('-published')[:10]
        return context


class InstallView(TemplateView):
    template_name = 'web/install.html'


class GettingStartedView(TemplateView):
    template_name = 'web/getting-started.html'
