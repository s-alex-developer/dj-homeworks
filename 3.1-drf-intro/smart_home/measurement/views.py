# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from rest_framework import generics

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, MeasurementSerializer, SensorDetailSerializer


class SensorAPIList(generics.ListCreateAPIView):

    """
        POST-запрос: Создать датчик. Указываются название и описание датчика. ( Задание 1 )

        GET-запрос: Получить список датчиков. Выдаётся список с краткой информацией по датчикам: ID,
        название и описание. ( Задание 4 )
    """

    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorAPIUpdate(generics.RetrieveUpdateAPIView):

    """
        GET-запрос: Получить информацию по конкретному датчику. Выдаётся полная информация по датчику: ID,
        название, описание и список всех измерений с температурой и временем. ( Задание 5 )

        PUT-запрос: Изменить датчик. Указываются название и описание. ( Задание 2 )
    """

    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementAPIView(generics.CreateAPIView):

    """
        POST-запрос: Добавить измерение. Указываются ID датчика и температура. ( Задание 3 )
    """

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer










