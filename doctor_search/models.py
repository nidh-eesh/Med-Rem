from django.db import models
from register_pat.models import Gender

# Create your models here.
class AvailableTime(models.Model):
    time = models.TimeField()

    def __str__(self):
        return str(self.time)

class Speciality(models.Model):
    speciality = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Speciality"
        ordering = ['speciality']

    def __str__(self):
        return self.speciality

class DayOfWeek(models.Model):
    day_of_week = models.CharField(max_length=10)

    def __str__(self):
        return self.day_of_week

    class Meta:
        ordering = ['id']

class DocSearch(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.ForeignKey(Speciality,on_delete=models.PROTECT)
    availability = models.BooleanField()
    gender = models.ForeignKey(Gender,on_delete=models.PROTECT)
    day_of_week = models.ManyToManyField(DayOfWeek)
    start_time=models.ForeignKey(AvailableTime,on_delete=models.PROTECT,related_name='+',)
    end_time=models.ForeignKey(AvailableTime,on_delete=models.PROTECT,related_name='+',)
    mobile = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Doctor Availability"
        ordering = ['name']

    def __str__(self):
        return self.name

