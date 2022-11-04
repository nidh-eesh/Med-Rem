from django.db import models
from medicine.models import MedicineRecord
# Create your models here.

class MedicineTime(models.Model):
    time = models.TimeField()



class PatientRec(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    date = models.DateField()
    gender = models.CharField(max_length=10)
    medicond = models.TextField()
    medicine_rec = models.ForeignKey(MedicineRecord,on_delete=models.PROTECT,null=True)
    dosage = models.IntegerField()
    medicine_time=models.ManyToManyField(MedicineTime)
    mobile = models.CharField(max_length=15)
    appoint_date = models.DateTimeField()

    def __str__(self):
        return self.name