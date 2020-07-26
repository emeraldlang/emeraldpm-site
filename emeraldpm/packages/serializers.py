from rest_framework import exceptions, serializers
from rest_framework.fields import CurrentUserDefault, get_attribute

from .models import Package, Version


class PackageVersionField(serializers.RelatedField):
    def to_internal_value(self, value):
        package_name, version = value.split('@')
        return self.get_queryset().get(
            package__name=package_name,
            version=version)

    def to_representation(self, value):
        return '%s@%s' % (value.package.name, value.version)


class CustomSlugRelatedField(serializers.SlugRelatedField):
    """
    Extends the SlugRelatedField class to allow the use of
    different sources for read/writes.
    """
    def __init__(self, read_source=None, **kwargs):
        self.read_source = read_source
        super().__init__(**kwargs)

    def get_attribute(self, instance):
        if self.read_source:
            return get_attribute(instance, self.read_source.split('.'))

        return super().get_attribute(instance)


class VersionSerializer(serializers.ModelSerializer):
    name = CustomSlugRelatedField(
        slug_field='name',
        read_source='package', # we can now write without nesting name in another object
        queryset=Package.objects.all())
    dependencies = PackageVersionField(
        many=True,
        queryset=Version.objects.all())

    class Meta:
        model = Version
        fields = (
            'name',
            'version',
            'archive',
            'description',
            'readme',
            'repository_url',
            'dependencies',
        )

    def to_internal_value(self, data):
        Package.objects.get_or_create(
            name=data['name'],
            defaults={'owner': self.context['request'].user})
        return super().to_internal_value(data)

    def validate_name(self, value):
        current_user = self.context['request'].user
        if value.owner != current_user:
            raise exceptions.PermissionDenied('You do not own this package.')
        return value

    def create(self, validated_data):
        name = validated_data.pop('name')
        dependencies = validated_data.pop('dependencies')
        version = Version.objects.create(
            package=name,
            **validated_data)
        version.dependencies.set(dependencies)
        return version


class PackageSerializer(serializers.ModelSerializer):
    versions = VersionSerializer(many=True, read_only=True)
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Package
        fields = ('name', 'owner', 'versions',)

    def get_owner(self, obj):
        return obj.owner.username
