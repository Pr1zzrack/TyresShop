from drf_spectacular.utils import extend_schema, extend_schema_field, OpenApiParameter, OpenApiExample
from rest_framework import viewsets
from .models import Tyre
from .serializers import TyreSerializer
from .filters import TyreFilter


class TyreViewSet(viewsets.ModelViewSet):
    queryset = Tyre.objects.all()
    serializer_class = TyreSerializer
    filterset_class = TyreFilter

    @extend_schema(
        description="Получить список всех шин с возможностью фильтрации",
        # parameters=[
        #     OpenApiParameter(
        #         name='season',
        #         description="Фильтр по сезону шин",
        #         required=False,
        #         type=str,
        #         examples=[
        #             OpenApiExample(
        #                 name="Зимние",
        #                 value="Зимние",
        #             ),
        #             OpenApiExample(
        #                 name="Летние",
        #                 value="Летние",
        #             ),
        #             OpenApiExample(
        #                 name="Всесезонные",
        #                 value="Всесезонные",
        #             ),
        #         ],
        #     ),
        #     OpenApiParameter(
        #         name='brand',
        #         description="Фильтр по бренду шин",
        #         required=False,
        #         type=str,
        #         examples=[
        #             OpenApiExample(
        #                 name="Nokian_Tyres",
        #                 value="Nokian_Tyres",
        #             ),
        #             OpenApiExample(
        #                 name="Michelin",
        #                 value="Michelin",
        #             ),
        #             OpenApiExample(
        #                 name="Bridgestone",
        #                 value="Bridgestone",
        #             ),
        #         ],
        #     ),
        #     OpenApiParameter(
        #         name='price',
        #         description="Фильтр по цене (например, price__gte=10000)",
        #         required=False,
        #         type=int,
        #     ),
        # ],
        responses={
            200: TyreSerializer(many=True),
            400: "Некорректный запрос",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="Создать новую запись о шине",
        request=TyreSerializer,
        responses={
            201: TyreSerializer,
            400: "Некорректные данные",
        },
        examples=[
            OpenApiExample(
                name="Пример создания шины",
                value={
                    "season": "Зимние",
                    "brand": "Nokian_Tyres",
                    "product_name": "Hakkapeliitta 9 SUV",
                    "price": "17 370 ₽",
                    "speed_index": "T",
                    "load_index": "103",
                    "width": "215",
                    "height": "65.0",
                    "diameter": "17",
                    "availability": "В наличии",
                    "images": [
                        "https://blacktyres.ru/media/images/tires/1115-nokian-tyres-hakkapeliitta-9-suv_big_1735395356.jpg?v=1740062445"
                    ],
                    "url": "https://blacktyres.ru/catalog-tyres/vendor/Nokian_Tyres/model-1115/31858/"
                },
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Получить детальную информацию о шине по её ID",
        responses={
            200: TyreSerializer,
            404: "Шина не найдена",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description="Обновить информацию о шине по её ID",
        request=TyreSerializer,
        responses={
            200: TyreSerializer,
            400: "Некорректные данные",
            404: "Шина не найдена",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        description="Частично обновить информацию о шине по её ID",
        request=TyreSerializer,
        responses={
            200: TyreSerializer,
            400: "Некорректные данные",
            404: "Шина не найдена",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description="Удалить запись о шине по её ID",
        responses={
            204: "Шина успешно удалена",
            404: "Шина не найдена",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
