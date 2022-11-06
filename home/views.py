from django.shortcuts import render,redirect
from register_pat.models import PatientRec
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/')
def home(request):
    return render(request, 'index.html')

@login_required(login_url='/')
def records(request):
    if request.method == 'POST':
        appoint_date = (request.POST['appoint_date'])
        print(appoint_date)
        patient_id=(request.POST['patient_id'])
        print(patient_id)
        try:
            patients = PatientRec.objects.filter(pk=patient_id).update(appoint_date=appoint_date)
        except:
            pass
        return redirect('/records/')
    patients = PatientRec.objects.all().order_by('id')
    return render(request, "records.html", {'patients' : patients} )