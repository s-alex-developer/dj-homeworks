from rest_framework import response
from rest_framework import viewsets
from rest_framework import pagination
from rest_framework import throttling
from rest_framework import permissions
from rest_framework.decorators import action

from django.db.models import Q
from django_filters import DateFromToRangeFilter
from django_filters.rest_framework import FilterSet

from .models import Advertisement
from .permissions import AdvertisementObjectPermission
from .serializers import AdvertisementModelSerializer, FavoriteModelSerializer


class AdvertisementFilter(FilterSet):

    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['status', "creator"]


class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementModelSerializer

    permission_classes = [
        AdvertisementObjectPermission,
        permissions.IsAuthenticatedOrReadOnly
    ]

    throttle_classes = [
        throttling.UserRateThrottle,
        throttling.AnonRateThrottle
    ]

    filterset_class = AdvertisementFilter
    pagination_class = pagination.PageNumberPagination

    def list(self, request, *args, **kwargs):

        # Аутентифицированный пользователь-Администратор видит всех пользователей объявления с любыми статусами:
        if request.auth and request.user.is_superuser:
            queryset = self.queryset

        # Аутентифицированный пользователь видит объявления всех пользователей со статусами "OPEN" и "CLOSE",
        # и все свои объявления со статусом "DRAFT"
        elif request.auth:
            queryset = Advertisement.objects.filter(~Q(status='DRAFT') |
                                                    Q(status='DRAFT') & Q(creator=request.user))

        # Не аутентифицированный пользователь видит объявления всех пользователей со статусами "OPEN", "CLOSE":
        if not request.auth:
            queryset = Advertisement.objects.filter(~Q(status='DRAFT'))

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    # Получить все избранные объявления конкретного пользователя:
    @action(detail=False, methods=["GET"], )
    def favorites(self, request):

        queryset = Advertisement.objects.filter(favorites__user_id=request.user)

        queryset = self.filter_queryset(queryset)

        serializer = self.serializer_class(data=queryset, many=True)
        serializer.is_valid()

        return response.Response(serializer.data)

    @action(detail=False, methods=['POST'], serializer_class=FavoriteModelSerializer)
    def add_favorite(self, request, ):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save(user_id=request.user.id)

        return response.Response(serializer.data)













    # Добавить объявление в избранное
    # @action(detail=False, methods=['POST'], serializer_class=FavoriteModelSerializer)
    # def favorite(self, request, ):
    #
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user_id=request.user.id)
    #
    #     return response.Response(serializer.data)

