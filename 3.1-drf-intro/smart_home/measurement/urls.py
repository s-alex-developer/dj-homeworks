from django.urls import path

from measurement.views import *

urlpatterns = [
    path('sensors/', SensorAPIList.as_view()),
    path('measurements/', MeasurementAPIView.as_view()),
    path('sensors/<int:pk>/', SensorAPIUpdate.as_view()),
]
