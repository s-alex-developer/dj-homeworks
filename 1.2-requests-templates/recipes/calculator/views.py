from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def recipes_view(request, recipe):

    servings = request.GET.get('servings')

    products_amount = {}

    if servings is None:
        servings = 1

    try:
        for ingridient, amount in DATA[f"{recipe}"].items():
            products_amount[f'{ingridient}'] = amount * int(servings)

    except:
        pass

    context = {
        'recipe': products_amount,
    }

    return render(request, 'calculator/index.html', context)
