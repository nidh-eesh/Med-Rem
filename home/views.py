from django.shortcuts import render
from register_pat.models import PatientRec
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/')
def home(request):
    return render(request, 'index.html')

def appointment(request):
    return render(request, 'appointment.html')

def records(request):
    patients = PatientRec.objects.all()
    return render(request, "records.html", {'patients' : patients} )