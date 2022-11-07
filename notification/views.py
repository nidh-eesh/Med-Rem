from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from medrem.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from register_pat.models import PatientRec
from doctor_search.models import DocSearch, DayOfWeek, Speciality
from datetime import datetime
from doctor_search.views import doctor_search,doctor_search_speciality
import re

# Create your views here.


@csrf_exempt
# Recieve WhatsApp Messages
def webflow(request):
    user = request.POST.get('From')
    message = request.POST.get('Body')
    print(f'{user} says {message}')

    # Check if Appointment is included in message
    appoint_msg = ['Appointment', 'appointment', 'appointmnt',
                   'Appointmnt', 'appoinment', 'Appoinment']
    for i in appoint_msg:
        if i in message:
            patient_ids = PatientRec.objects.values_list('id', flat=True)
            # Check if ID exists in list
            parsed_id = int(re.search(r'\d+', message).group())
            if PatientRec.objects.filter(id=parsed_id).exists():
                for id in patient_ids:
                    message1 = i+" {}".format(id)
                    mobile = user[12:]
                    if PatientRec.objects.get(id=parsed_id).mobile == mobile:
                        if message == message1:
                            appointment_fetch(user, id)
                            response = MessagingResponse()
                            return HttpResponse(str(response))
                    else:
                        response = MessagingResponse()
                        response.message(
                            'Please try from registered mobile number')
                        return HttpResponse(str(response))
            else:
                response = MessagingResponse()
                response.message('ID does not exist')
                return HttpResponse(str(response))
    doctor_search_msg = ['Search Doctors', 'search doctors', 'search doctrs ', 'search Doctors',
                         'search docs', 'Search docs', 'search Docs', 'Search Doctor', 'search doctor', 
                         'search doctr ', 'search Doctor', 'search doc', 'Search doc', 'Search Doc', 'search Doc',
                         'Search doctr', 'Doc search', 'Doc Search', 'Doctor Availablity', 'Doctors', 'doctors','Doctor availablity'
                         'Available Doctors', 'available doctors', 'Find Doctor', 'Doctor search', 'Doctor Search']
    mobile = user[12:]
    doctor_specialities= Speciality.objects.values_list('speciality', flat=True)
    if any(i in message for i in doctor_search_msg):
        for j in doctor_specialities:
            if(j in message):
                doctor_search_speciality(mobile,j)
                response = MessagingResponse()
                return HttpResponse(str(response))
        doctor_search(mobile)
        response = MessagingResponse()
        return HttpResponse(str(response))
    doctor_speciality_list = ''
    for i in doctor_specialities:
        print(i)
        doctor_speciality_list = doctor_speciality_list+'\n'+str(i)
    response = MessagingResponse()
    response.message(
        """Available Servicies: 
        \nFor appointment details send \'Appointment<space>ID\'
        \nFor all doctor\'s schedule send \'Search Doctors\'
        \nTo search doctors based on speciality send Doctor\n Available specialities : {}""".format(doctor_speciality_list))
    return HttpResponse(str(response))

# Send WhatsApp Messages

# Appointment


def appointment(mobile, appoint_date):

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Your appointment is scheduled on {}'.format(appoint_date),
        to='whatsapp:+91{}'.format(mobile))
    print(mobile)
    print(message.sid)

# Appointment Re-Fetch


def appointment_fetch(mobile, id):

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    appoint_dates = PatientRec.objects.values_list(
        'appoint_date', flat=True).filter(id=id)
    for appoint_date in appoint_dates:
        appoint_date = str(appoint_date)
        appoint_date = datetime.strptime(
            appoint_date, '%Y-%m-%d %H:%M:%S').strftime('%b %d %I:%M %p')
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Your appointment is scheduled on {}'.format(appoint_date),
        to='{}'.format(mobile))
    print(mobile)
    print(message.sid)
