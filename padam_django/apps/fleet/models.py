from django.db import models
from padam_django.apps.geography.models import Place
from django.db.models import Max, Min
from django.contrib import admin


class Driver(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='driver')

    def __str__(self):
        return f"Driver: {self.user.username} (id: {self.pk})"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return f"Bus: {self.licence_plate} (id: {self.pk})"


class BusShift(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.PROTECT)  # PROTECT because a bus shift cannot not have a bus. User must change the bus of the busShift before deleting the bus
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT)  # idem

    def __str__(self):
        return f"{self.driver} {self.bus}  (id: {self.pk}) "

    @admin.display(
        description='Departure Time',
    )
    def departure_time(self):
        departure = BusStop.objects.filter(busShift=self.pk).aggregate(Min('time'))['time__min']
        return departure

    @admin.display(
        description='Arrival Time',
    )
    def arrival_time(self):
        arrival = BusStop.objects.filter(busShift=self.pk).aggregate(Max('time'))['time__max']
        return arrival

    @admin.display(
        description='Travel Time',
    )
    def travel_time(self):
        travel_time = self.arrival_time() - self.departure_time()
        return travel_time


class BusStop(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    busShift = models.ForeignKey(BusShift, on_delete=models.CASCADE)
    time = models.DateTimeField()
