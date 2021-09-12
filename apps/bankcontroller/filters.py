import django_filters as filters

from .models import Service


class ServiceFilter(filters.FilterSet):

    currency = filters.ChoiceFilter(choices=Service.CUREENCY)
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')
    purchased = filters.BooleanFilter(
        field_name='shop__service', lookup_expr='isnull',
        method='filter_service_in_shop_service', label='Приобретено'
    )

    # не работатет false
    def filter_service_in_shop_service(self, queryset, name, value):
        lookup = '__'.join([name, 'isnull'])
        return queryset.exclude(
            **{lookup: value}
        ).filter(
            shop__user=self.request.user,
        )
