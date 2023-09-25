import csv

from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect


from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations_view(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице

    with open(BUS_STATION_CSV) as file:
        data = csv.DictReader(file)

        bus_stations = []
        station = {}

        for element in data:
            station['Name'] = element['Name']
            station['Street'] = element['Street']
            station['District'] = element['District']

            bus_stations.append(station)
            station = {}

    page_number = int(request.GET.get('page', 1))

    paginator = Paginator(bus_stations, 10)

    page = paginator.get_page(page_number)

    context = {
        'page': page,
    }

    return render(request, 'stations/index.html', context)
