# Generated by Django 5.1.6 on 2025-03-14 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tyre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.CharField(max_length=50, verbose_name='Сезон')),
                ('brand', models.CharField(max_length=255, verbose_name='Бренд')),
                ('product_name', models.CharField(max_length=255, verbose_name='Название продукта')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('speed_index', models.CharField(max_length=50, verbose_name='Индекс скорости')),
                ('load_index', models.CharField(max_length=50, verbose_name='Индекс нагрузки')),
                ('width', models.IntegerField(null=True, verbose_name='Ширина')),
                ('height', models.IntegerField(null=True, verbose_name='Высота')),
                ('diameter', models.FloatField(null=True, verbose_name='Диаметр')),
                ('availability', models.CharField(max_length=50, verbose_name='Наличие')),
                ('images', models.JSONField(verbose_name='Изображения')),
                ('url', models.URLField(verbose_name='Ссылка на продукт')),
            ],
        ),
    ]
