from django.contrib import admin
from .models import Tyre


class TyreAdmin(admin.ModelAdmin):
    list_display = ('brand', 'product_name', 'season', 'price', 'availability')
    search_fields = ('brand', 'product_name', 'season')
    list_filter = ('season', 'brand', 'availability')
    fieldsets = (
        (None, {
            'fields': ('season', 'brand')
        }),
        ('Информация о продукте', {
            'fields': ('product_name', 'price', 'speed_index', 'load_index', 'width', 'height', 'diameter', 'availability', 'images', 'url')
        }),
    )

admin.site.register(Tyre, TyreAdmin)
