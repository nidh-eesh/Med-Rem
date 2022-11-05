from django.db import models

# Create your models here.
class AvailableTime(models.Model):
    time = models.TimeField()

    def __str__(self):
        return str(self.time)

class DocSearch(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    availability = models.BooleanField()
    gender = models.CharField(max_length=10)
    day_of_week = models.CharField(max_length=10)
    start_time=models.ForeignKey(AvailableTime,on_delete=models.SET_NULL,null=True,related_name='+',)
    end_time=models.ForeignKey(AvailableTime,on_delete=models.SET_NULL,null=True,related_name='+',)
    mobile = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Doctor Availability"

    def __str__(self):
        return self.name

    