import django_filters


def get_filterset_base(Model):
    class MediaModelFilter(django_filters.FilterSet):
        modified__gt = django_filters.IsoDateTimeFilter(field_name='modified', lookup_expr='gt')

        class Meta:
            model = Model
            fields = {
                'id': ['exact'],
                "title": ['icontains'],
                "description": ['icontains'],
                "modified": ['exact', 'gt'],
                "created": ['exact'],
                "status": ['exact'],
                "parent_id": ['exact'],
                "parent_type_id": ['exact'],
                "category": ['exact'],
                "origin_url": ['exact'],
                "origin_id": ['exact'],
                "content_type": ['exact'],
            }

    return MediaModelFilter
