from datetime import date, timedelta

from django.conf import settings
from django.core.validators import validate_slug, FileExtensionValidator
from django.db import models

from .fields import VersionNumber, VersionNumberField


class Package(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        validators=[validate_slug,])
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='packages')

    @property
    def num_downloads_last_week(self):
        return self._get_num_downloads(timedelta(weeks=1))

    @property
    def num_downloads_last_30_days(self):
        return self._get_num_downloads(timedelta(days=30))

    def _get_num_downloads(self, td):
        return self.download_counts\
            .filter(day__gt=date.today() - td)\
            .aggregate(count=models.Sum('count'))['count'] or 0

    def __str__(self):
        return self.name


def version_default():
    return VersionNumber(0)


def file_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/plugins/<plugin_slug>/<plugin_slug>-<version>.zip
    return 'packages/%s/%s-%s.zip' % (
        instance.package.name,
        instance.package.name,
        instance.version)


class Version(models.Model):
    version = VersionNumberField(default=version_default)
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name='versions')
    published = models.DateTimeField(editable=False, auto_now_add=True)
    archive = models.FileField(
        upload_to=file_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['zip'])])
    description = models.TextField(max_length=4096, blank=True)
    readme = models.TextField(blank=True)
    repository_url = models.URLField(blank=True)

    dependencies = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='dependents',
        blank=True)

    class Meta:
        indexes = (
            models.Index(fields=('published',)),
            models.Index(fields=('package',)),
        )
        unique_together = ('version', 'package')
        get_latest_by = 'published'
        ordering = ['-version']

    def __str__(self):
        return '%s@%s' % (self.package.name, str(self.version))


class DownloadCount(models.Model):
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name='download_counts')
    day = models.DateField(editable=False, auto_now_add=True)
    count = models.BigIntegerField(default=0)

    class Meta:
        indexes = (
            models.Index(fields=('day',)),
            models.Index(fields=('package',)),
        )
        unique_together = ('day', 'package')

    def __str__(self):
        return '%s: %d on %s' % (self.package, self.count, self.day)
