from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    # при необходимости добавьте параметры фильтрации
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class CustomSearchFilter(SearchFilter):

    search_param = 'products'

    # Переопределение метода get_search_fields() для дополнительного задания.
    # Выполнил согласно документации, НЕ РАБОТАЕТ!!!
    # По отдельности поиски с параметрами запроса search и products работают.
    # Реализовать параллельную работу параметров не удалось...
    def get_search_fields(self, view, request):

        if request.query_params.get('search'):
            return ['products__title', 'products__description']

        return getattr(view, 'search_fields', None)


class StockViewSet(ModelViewSet):

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    pagination_class = PageNumberPagination

    # при необходимости добавьте параметры фильтрации
    filter_backends = [CustomSearchFilter]
    search_fields = ['products__id']



