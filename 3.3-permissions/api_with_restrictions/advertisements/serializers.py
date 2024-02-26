from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, Favorite


class UserModelSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name')


class AdvertisementModelSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserModelSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):

        """Метод для валидации. Вызывается при создании и обновлении."""
        # TODO: добавьте требуемую валидацию

        users_open_ads = Advertisement.objects.filter(creator=self.context["request"].user.id,
                                                      status='OPEN').count()
        # print(self.context["request"].method)
        if users_open_ads == 10 and self.context["request"].method == 'POST':
            raise Exception('Превышено максимальное число активных объявлений для данного пользователя')

        return data


class FavoriteModelSerializer(serializers.ModelSerializer):

    advertisement_id = serializers.IntegerField()

    class Meta:
        model = Favorite
        fields = ('id', 'advertisement_id', 'user_id')

    def create(self, validated_data):

        adv_creator = Advertisement.objects.get(pk=validated_data.get('advertisement_id')).creator.id
        request_user_id = validated_data.get('user_id')

        favorite_ads_id = []

        for adv in Favorite.objects.filter(user_id=request_user_id):
            favorite_ads_id.append(adv.advertisement_id)

        if not adv_creator == request_user_id and not \
                validated_data.get('advertisement_id') in favorite_ads_id:

            return Favorite.objects.create(**validated_data)

        elif adv_creator == request_user_id:
            raise Exception('Нельзя сохранять свои объявления в Избранное.')

        elif validated_data.get('advertisement_id') in favorite_ads_id:
            raise Exception('Данное объявление уже сохранено в Избранном.')

