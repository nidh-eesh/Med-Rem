from django.db import models

# Create your models here.

class MedicineRecord(models.Model):
    medicine_name=models.CharField(max_length=100)
