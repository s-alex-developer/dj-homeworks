from django.db import models


class Phone(models.Model):

    # TODO: Добавьте требуемые поля
    name = models.CharField('Модель', max_length=50)
    price = models.DecimalField('Стоимость', max_digits=7, decimal_places=1)
    image = models.CharField('Изображение', max_length=255)
    release_date = models.DateField('Дата релиза', null=True)
    lte_exists = models.BooleanField('Поддержка LTE', null=True)
    slug = models.SlugField('Слизняк :)', unique=True, db_index=True)
