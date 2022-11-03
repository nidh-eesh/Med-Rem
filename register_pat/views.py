from django.shortcuts import render,redirect
from .models import *
from medicine.models import MedicineRecord
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from notification.views import appointment
from datetime import datetime

# Create your views here.
@login_required(login_url='/')
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        date = request.POST['date']
        appoint_date = request.POST['appoint_date']
        gender = request.POST['inlineRadioOptions']
        medicond = request.POST['medicalCondition']
        medicine = request.POST['medicine']
        dosage = request.POST['dosage']        
        mobile = request.POST['mobileNumber']
        timeofdaychar = request.POST.getlist('timeofday')
        timeofday = [eval(i) for i in timeofdaychar]
        perday=len(timeofday)
        #Save data to database
        times = MedicineTime.objects.all()
        patientRec = PatientRec.objects.create(name=name, age=age,date=date,appoint_date=appoint_date,gender=gender,
                                                dosage=dosage,medicine_rec_id=medicine,medicond=medicond,
                                                perday=perday,mobile=mobile)
        for time in times:
            if time.id in timeofday:
                patientRec.medicine_time.add(time)
                                                    
            
        patientRec.save()
        messages.success(request, 'Record Saved')
    
        #Convert Date Format
        appoint_date = datetime.strptime(appoint_date, '%Y-%m-%dT%H:%M').strftime('%b %d %I:%M %p')

        #Send WhatsApp Message
        appointment(mobile,appoint_date)
        return redirect('/register/')
    medicines = MedicineRecord.objects.all().order_by('medicine_name')
    return render(request, 'register.html', {'medicines' : medicines} )

