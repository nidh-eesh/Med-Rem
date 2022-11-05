from django.contrib import admin
from .models import *

# Register your models here.
class DocSearchAdmin(admin.ModelAdmin):
    filter_horizontal = ['day_of_week']
admin.site.register(DocSearch ,DocSearchAdmin)
admin.site.register(Speciality)