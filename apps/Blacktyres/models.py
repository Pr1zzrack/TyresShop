from django.db import models


class Tyre(models.Model):
    season = models.CharField(max_length=50, verbose_name="Сезон")
    brand = models.CharField(max_length=255, verbose_name="Бренд")
    product_name = models.CharField(max_length=255, verbose_name="Название продукта")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    speed_index = models.CharField(max_length=50, verbose_name="Индекс скорости")
    load_index = models.CharField(max_length=50, verbose_name="Индекс нагрузки")
    width = models.IntegerField(verbose_name="Ширина", null=True)
    height = models.IntegerField(verbose_name="Высота", null=True)
    diameter = models.FloatField(verbose_name="Диаметр", null=True)
    availability = models.CharField(max_length=50, verbose_name="Наличие")
    images = models.JSONField(verbose_name="Изображения")
    url = models.URLField(verbose_name="Ссылка на продукт")

    def __str__(self):
        return f"{self.brand} - {self.product_name}"
    
    class Meta:
        verbose_name = 'Шина'
        verbose_name_plural = 'Шины'
