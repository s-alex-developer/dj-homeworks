from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    # при необходимости добавьте параметры фильтрации
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']

    # _________Дополнительная функция для ДЗ "CI/CD"__________
    @action(detail=False, methods=['GET'])
    def show(self, request):
        """ Возвращает продукт с указанным id """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        product_id = 1
        response = Product.objects.get(id=product_id)
        serializer = self.serializer_class(response)

        return Response(serializer.data)
    # __________________________________________________________


class StockViewSet(ModelViewSet):

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    pagination_class = PageNumberPagination

    # при необходимости добавьте параметры фильтрации
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = ['products']
    search_fields = ['products__title', 'products__description']
