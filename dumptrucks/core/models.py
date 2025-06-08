from django.db import models

class Truck(models.Model):
    number = models.CharField(max_length=10)
    model = models.CharField(max_length=50)
    max_capacity = models.FloatField()
    current_weight = models.FloatField()
    sio2_pct = models.FloatField()
    fe_pct = models.FloatField()

    def overload(self):
        return max(0, (self.current_weight - self.max_capacity) / self.max_capacity * 100)

class UnloadPoint(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()

class Stock(models.Model):
    name = models.CharField(max_length=50, default="Склад")
    volume = models.FloatField()
    sio2_pct = models.FloatField()
    fe_pct = models.FloatField()