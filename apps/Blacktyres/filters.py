import django_filters
from .models import Tyre


class TyreFilter(django_filters.FilterSet):
    season = django_filters.CharFilter(field_name='season', lookup_expr='iexact', label='Сезон')
    brand = django_filters.CharFilter(field_name='brand', lookup_expr='iexact', label='Бренд')
    product_name = django_filters.CharFilter(field_name='product_name', lookup_expr='icontains', label='Название продукта')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Цена до')
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    speed_index = django_filters.CharFilter(field_name='speed_index', lookup_expr='iexact', label='Индекс скорости')
    load_index = django_filters.CharFilter(field_name='load_index', lookup_expr='iexact', label='Индекс нагрузки')
    width_lte = django_filters.NumberFilter(field_name='width', lookup_expr='lte', label='Ширина до')
    width_gte = django_filters.NumberFilter(field_name='width', lookup_expr='gte', label='Ширина от')
    height_lte = django_filters.NumberFilter(field_name='height', lookup_expr='lte', label='Высота до')
    height_gte = django_filters.NumberFilter(field_name='height', lookup_expr='gte', label='Высота от')
    diameter_lte = django_filters.NumberFilter(field_name='diameter', lookup_expr='lte', label='Диаметр до')
    diameter_gte = django_filters.NumberFilter(field_name='diameter', lookup_expr='gte', label='Диаметр от')
    availability = django_filters.CharFilter(field_name='availability', lookup_expr='iexact', label='Наличие')

    class Meta:
        model = Tyre
        fields = [
            'season', 'brand', 'product_name', 'price_lte', 'price_gte',
            'speed_index', 'load_index', 'width_lte', 'width_gte',
            'height_lte', 'height_gte', 'diameter_lte', 'diameter_gte', 'availability'
        ]
