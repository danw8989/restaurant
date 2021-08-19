
import django_filters
from django_filters.filters import OrderingFilter, CharFilter
from api.models import Menu


class MenuFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='icontains', )
    created_at_gt = django_filters.DateFilter(field_name='created_at', lookup_expr='gt')
    created_at_lt = django_filters.DateFilter(field_name='created_at', lookup_expr='lt')
    modified_at = django_filters.DateFilter(field_name='modified_at', lookup_expr='icontains')
    modified_at_gt = django_filters.DateFilter(field_name='modified_at', lookup_expr='gt')
    modified_at_lt = django_filters.DateFilter(field_name='modified_at', lookup_expr='lt')
    title_search = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    order_by = OrderingFilter(
        fields=(
            ("title", "title"),
            ('dishes', 'dishes_count'),
        ),

    )
    class Meta:
        model = Menu
        fields = []
