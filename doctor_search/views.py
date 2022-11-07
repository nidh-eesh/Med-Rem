from twilio.rest import Client
from medrem.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from doctor_search.models import DocSearch, DayOfWeek
# Create your views here.

# Doctor Search

def doctor_search(mobile):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    doctors = DocSearch.objects.filter(availability=True)
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
            body='Doctor Name : {}\nSpeciality : {}\nGender : {}\nAvailable Days : {}\nOP start time : {}\nOP end time : {}\nContact : {}'.format(
                doctor.name, doctor.speciality, doctor.gender, avail_day_list, doctor.start_time, doctor.end_time, doctor.mobile),
            to='whatsapp:+91{}'.format(mobile))
        print(mobile)
        print(message.sid)

def doctor_search_speciality(mobile,speciality):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    doctors = DocSearch.objects.filter(availability=True)
    days = DayOfWeek.objects.all()
    for doctor in doctors:
        if speciality==str(doctor.speciality):
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
                body='Doctor Name : {}\nSpeciality : {}\nGender : {}\nAvailable Days : {}\nOP start time : {}\nOP end time : {}\nContact : {}'.format(
                    doctor.name, doctor.speciality, doctor.gender, avail_day_list, doctor.start_time, doctor.end_time, doctor.mobile),
                to='whatsapp:+91{}'.format(mobile))
            print(mobile)
            print(message.sid)