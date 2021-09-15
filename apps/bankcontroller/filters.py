import django_filters as filters

from .models import Service, ShopService, MoneyTransfer


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


class UserInfoServiceLsitFilter(filters.FilterSet):

    date = filters.DateFilter(label='Дата', lookup_expr='contains')
    price__gt = filters.NumberFilter(
        field_name='service__price', lookup_expr='gt')
    price__lt = filters.NumberFilter(
        field_name='service__price', lookup_expr='lt')
    currency = filters.ChoiceFilter(
        choices=Service.CUREENCY, field_name='service__currency')

    class Meta:
        model = ShopService
        fields = ('date', 'service')


class UserInfoMoneyTransferFilter(filters.FilterSet):

    date = filters.DateFilter(label='Дата', lookup_expr='contains')
    price__gt = filters.NumberFilter(
        field_name='amount', lookup_expr='gt')
    price__lt = filters.NumberFilter(
        field_name='amount', lookup_expr='lt')
    name = filters.CharFilter(
        label='Пользователь',
        lookup_expr='contains',
        field_name='user_received'
    )

    class Meta:
        model = MoneyTransfer
        fields = ('user_received',)
