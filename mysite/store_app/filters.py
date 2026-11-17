import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.NumberFilter(field_name='subcategory__category')
    name = django_filters.CharFilter(field_name='product_name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['subcategory', 'product_type']