from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from medrem.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from register_pat.models import PatientRec
from doctor_search.models import DocSearch, DayOfWeek
from datetime import datetime
import re

# Create your views here.


@csrf_exempt
# Recieve WhatsApp Messages
def webflow(request):
    user = request.POST.get('From')
    message = request.POST.get('Body')
    print(f'{user} says {message}')

    # Check if Appointment is included in message
    if ('appointment' or 'Appointment') in message:
        print(message)
        patient_ids = PatientRec.objects.values_list('id', flat=True)
        # Check if ID exists in list
        parsed_id = int(re.search(r'\d+', message).group())
        if PatientRec.objects.filter(id=parsed_id).exists():
            for id in patient_ids:
                message1 = "appointment {}".format(id)
                message2 = "Appointment {}".format(id)
                mobile = user[12:]
                if PatientRec.objects.get(id=parsed_id).mobile == mobile:
                    if message == message1 or message == message2:
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
    elif ('Doctor Availability' or 'doctor availability') in message:
        mobile = user[12:]
        doctor_search(mobile)
        response = MessagingResponse()
        return HttpResponse(str(response))
    response = MessagingResponse()
    response.message(
        """Available Servicies: \nFor appointment details send \'Appointment<space>ID\' 
        \nFor Doctor\'s schedule send \'Doctor Availability\'""")
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


# Doctor Search

def doctor_search(mobile):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    doctors = DocSearch.objects.all()
    days = DayOfWeek.objects.all()
    for doctor in doctors:
        avail_day_list = ''
        for day in days:
            try:
                available_days = doctor.day_of_week.get(id=day.id)
                avail_day_list = avail_day_list+" , "+str(available_days) 
            except DayOfWeek.DoesNotExist:
                pass
        avail_day_list = avail_day_list[2:]        
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='Doctor Name : {}\nSpeciality : {}\nGender : {}\nAvailability : {}\nAvailable Days{}\nOP start time : {}\nOP end time : {}\nContact : {}'.format(doctor.name,doctor.speciality,doctor.gender,doctor.availability,avail_day_list,doctor.start_time,doctor.end_time,doctor.mobile),
            to='whatsapp:+91{}'.format(mobile))
        print(mobile)
        print(message.sid)