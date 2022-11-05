from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from medrem.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from register_pat.models import PatientRec, MedicineTime
from datetime import datetime
import re

# Create your views here.

@csrf_exempt

#Recieve WhatsApp Messages
def webflow(request):
    user = request.POST.get('From')
    message = request.POST.get('Body')
    print(f'{user} says {message}')

    #Check if Appointment is included in message
    for msg in message:
        if 'appointment' or 'Appointment' in msg:
            patient_ids=PatientRec.objects.values_list('id', flat=True)
            #Check if ID exists in list
            parsed_id=int(re.search(r'\d+', message).group())
            if PatientRec.objects.filter(id=parsed_id).exists():
                for id in patient_ids:
                    message1="appointment {}".format(id)
                    message2="Appointment {}".format(id)
                    mobile=user[12:]
                    if PatientRec.objects.get(id=parsed_id).mobile == mobile:
                        if message == message1 or message == message2:
                            appointment_fetch(user,id)
                            response = MessagingResponse()
                            return HttpResponse(str(response))
                    else:
                        response = MessagingResponse()
                        response.message('Please try from registered mobile number')
                        return HttpResponse(str(response))
            else:
                response = MessagingResponse()
                response.message('ID does not exist')
                return HttpResponse(str(response))                                              
    response = MessagingResponse()
    response.message('Thank for your message! A member of our team will be '
                        'in touch with you soon.')
    return HttpResponse(str(response))

#Send WhatsApp Messages

#Appointment

def appointment(mobile,appoint_date):
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='Your appointment is scheduled on {}'.format(appoint_date),
    to='whatsapp:+91{}'.format(mobile))
    print(mobile)
    print(message.sid)

#Appointment Re-Fetch

def appointment_fetch(mobile,id):

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    appoint_dates=PatientRec.objects.values_list('appoint_date',flat=True).filter(id=id)
    for appoint_date in appoint_dates:
        appoint_date=str(appoint_date)
        appoint_date = datetime.strptime(appoint_date, '%Y-%m-%d %H:%M:%S').strftime('%b %d %I:%M %p')
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='Your appointment is scheduled on {}'.format(appoint_date),
    to='{}'.format(mobile))
    print(mobile)
    print(message.sid)
