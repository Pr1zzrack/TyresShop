from rest_framework import serializers
from .models import Tyre


class TyreSerializer(serializers.ModelSerializer):
    season = serializers.CharField(help_text="Сезон шины (например, Зимние, Летние, Всесезонные)")
    brand = serializers.CharField(help_text="Бренд шины (например, Nokian_Tyres, Michelin)")
    product_name = serializers.CharField(help_text="Название модели шины")
    price = serializers.CharField(help_text="Цена шины")
    speed_index = serializers.CharField(help_text="Индекс скорости (например, T, H)")
    load_index = serializers.CharField(help_text="Индекс нагрузки (например, 95, 103)")
    width = serializers.CharField(help_text="Ширина шины (например, 215)")
    height = serializers.CharField(help_text="Высота профиля шины (например, 65.0)")
    diameter = serializers.CharField(help_text="Диаметр шины (например, 17)")
    availability = serializers.CharField(help_text="Наличие шины (например, В наличии, Нет в наличии)")
    images = serializers.JSONField(help_text="Ссылки на изображения шины")
    url = serializers.URLField(help_text="Ссылка на страницу продукта")

    class Meta:
        model = Tyre
        fields = '__all__'
