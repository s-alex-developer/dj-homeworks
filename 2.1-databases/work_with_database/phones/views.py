from django.shortcuts import render, redirect

from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):

    template = 'catalog.html'

    if request.GET.get('sort'):

        if request.GET.get('sort') == 'name':
            sort_param = 'name'

        if request.GET.get('sort') == 'min_price':
            sort_param = 'price'

        if request.GET.get('sort') == 'max_price':
            sort_param = '-price'

        phones = [{'name': phone_object.name, 'price': phone_object.price, 'image': phone_object.image,
                   'slug': phone_object.slug} for phone_object in Phone.objects.all().order_by(sort_param)]

    else:

        phones = [{'name': phone_object.name, 'price': phone_object.price, 'image': phone_object.image,
                   'slug': phone_object.slug} for phone_object in Phone.objects.all()]

    context = {'phones': phones}

    return render(request, template, context)


def show_product(request, slug):

    template = 'product.html'

    phone = {}

    for phone_object in Phone.objects.filter(slug=slug):

        phone['name'] = phone_object.name
        phone['image'] = phone_object.image
        phone['price'] = phone_object.price
        phone['release_date'] = phone_object.release_date
        phone['lte_exists'] = phone_object.lte_exists

    context = {'phone': phone}

    return render(request, template, context)


