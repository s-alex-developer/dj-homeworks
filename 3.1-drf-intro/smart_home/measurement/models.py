from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)


class Sensor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Measurement(models.Model):
    temperature = models.FloatField()
    measurement_time = models.DateTimeField(auto_now_add=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements_results')
    photo = models.ImageField(upload_to='measurement_photos/%Y/%m/%d/', max_length=255, null=True)



