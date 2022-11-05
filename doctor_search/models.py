from django.db import models

# Create your models here.
class DocSearch(models.Model):
    name = models.CharField(max_length=100)
    speciality = models.CharField(max_length=100)
    availability = models.BooleanField()
    gender = models.CharField(max_length=10)
    day_of_week = models.CharField(max_length=10)
    #avail_time=models.ManyToManyField(DocAvalTime)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.name