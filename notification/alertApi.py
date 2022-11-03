from datetime import datetime
from register_pat.models import PatientRec
from twilio.rest import Client
from medrem.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

#Live Update
def medicine_time_alert():

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    time = datetime.now().time().strftime("%H:%M")
    patient_rec = PatientRec.objects.all()
    for record in patient_rec:
        medicine_time = str(record.medicine_time.time)
        medicine_time = datetime.strptime(medicine_time, "%H:%M:%S").strftime("%H:%M")
        if medicine_time == time:
            message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body='It is time for your medicine {} Dosage:{}'.format(record.medicine_rec.medicine_name,record.dosage),
                    to='whatsapp:+91{}'.format(record.mobile))
            print(record.mobile)
            print(message.sid)