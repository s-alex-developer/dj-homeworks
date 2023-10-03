from django.db import models


class Phone(models.Model):

    # TODO: Добавьте требуемые поля
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=1)
    image = models.CharField(max_length=300)
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField()
