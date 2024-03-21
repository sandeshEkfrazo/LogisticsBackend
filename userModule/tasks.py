from celery import shared_task
from .models import *
from django_celery_beat.models import PeriodicTask
import datetime
from dateutil import parser
from logisticsapp.models import *
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
import geopy.distance
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import get_template
from django.shortcuts import render
import requests
from django.core.management import call_command
from logisticsapp import views
import json
from datetime import timedelta

@shared_task(bind=True)
def assignNewDriverAftertwoMinutesLast(self, *args, **kwargs):
    BookingDetail.objects.filter(order_id=kwargs['order_id']).update(status_id=13)

    return "success"


@shared_task(bind=True)
def assignNewDriverAftertwoMinutes(self, *args,  **kwargs):

    location_detail = kwargs['location_detail']
    data = kwargs['data']
    travel_details = kwargs['travel_details']
    sub_user_ph_number = kwargs['sub_user_ph_number']
    is_scheduled = kwargs['is_scheduled']

    if BookingDetail.objects.get(id=kwargs['booking_id']).status_id == 1:
        if Driver.objects.filter(vehicle__vehicletypes_id=data['vehicle_type'], is_online=True):
            driver_obj_location = Driver.objects.filter(
                vehicle__vehicletypes_id=data['vehicle_type'], is_online=True).values()

            finalArr = []
            final_obj = {}

            randomly_assigning_driver = []

            if type(location_detail) == dict:
                start_location = (
                    location_detail['start_location']['lat'], location_detail['start_location']['lng'])
            else:
                start_location = (
                    location_detail[0]['start_location']['lat'], location_detail[0]['start_location']['lng'])

            for i in driver_obj_location:

                end_location = (i['live_lattitude'], i['live_longitude'])

                final_obj['lat'] = i['live_lattitude']
                final_obj['lng'] = i['live_longitude']
                final_obj['total_km'] = geopy.distance.geodesic(
                    start_location, end_location).km
                final_obj['driver_id'] = i['user_id']
                finalArr.append(final_obj)
                final_obj = {}

                if ScheduledOrder.objects.filter(Q(booking__driver_id=i['user_id'])).exists():

                    s = ScheduledOrder.objects.filter(booking__driver_id=i['user_id']).values(
                        'scheduled_date_and_time').last()['scheduled_date_and_time']

                    if BookingDetail.objects.filter((Q(driver_id=i['user_id']) & (Q(status_id=1) | Q(status_id=2) | Q(status_id=6) | Q(status_id=8) | Q(status_id=10))) & Q(is_scheduled=True)).exists():

                        if s.date() == datetime.datetime.today().date():

                            print("dont assign", i['user_id'])
                            for j in finalArr:
                                if j.get('driver_id') == i['user_id']:
                                    finalArr.remove(j)
                                    break
                        else:
                            print("assign")
                            min_km = min(finalArr, key=lambda x: x['total_km'])

                            # print("min km==>", min_km)
                            randomly_assigning_driver.append(min_km)

                    else:
                        print("assign")
                        min_km = min(finalArr, key=lambda x: x['total_km'])

                        # print("min km==>", min_km)
                        randomly_assigning_driver.append(min_km)

                else:
                    print("1")
                    if BookingDetail.objects.filter(Q(driver_id=i['user_id']) & (Q(status_id=1) | Q(status_id=2) | Q(status_id=6) | Q(status_id=8) | Q(status_id=10))).exists():
                        print("dont assign", i['user_id'])
                        for j in finalArr:
                            if j.get('driver_id') == i['user_id']:
                                finalArr.remove(j)
                                break
                    else:
                        print("assign")
                        min_km = min(finalArr, key=lambda x: x['total_km'])

                        # print("min km==>", min_km)
                        randomly_assigning_driver.append(min_km)

            if (randomly_assigning_driver == [] or len(randomly_assigning_driver) == 0):
                msg = {'message': "all vehicles are busy in state please try after some time",
                       'status': 'ALREADY RESERVED'}
                return msg
            else:
                get_est_cost = views.find_vehicle_estimation_cost(
                    data, data['vehicle_type'], location_detail)

                if len(finalArr) != 0 and len(finalArr) > 1:

                    next_driver_details = [
                        entry for entry in finalArr if entry['driver_id'] != int(kwargs['old_driver_id'])]

                    print("next_driver_details==>", next_driver_details)

                    min_object = min(next_driver_details,
                                     key=lambda x: x['total_km'])

                    if BookingDetail.objects.filter(Q(order_id=kwargs['order_id']) & Q(driver_id=kwargs['old_driver_id'])).exists():

                        BookingDetail.objects.filter(order_id=kwargs['order_id']).update(
                            driver_id=min_object['driver_id'],
                            assigned={'old_driver_id': kwargs['old_driver_id']}
                        )

                        current_time = datetime.datetime.now()

                        new_time = current_time + timedelta(minutes=2, seconds=30)

                        clocked_obj = ClockedSchedule.objects.create(
                            clocked_time=new_time
                        )

                        PeriodicTask.objects.create(name="assignNewDriverAftertwoMinutesLast"+str(clocked_obj.id), task="userModule.tasks.assignNewDriverAftertwoMinutesLast", clocked_id=clocked_obj.id, one_off=True, kwargs=json.dumps(
                            {
                                'order_id': kwargs['order_id']
                            }
                        ))

                else:
                    msg = {'message': "no driver found near you"}

                msg = {'message': 'wait till the driver accepts your order',
                       'data': finalArr, 'order_id': kwargs['order_id']}
                return msg

        msg = {'message': 'no vehicle found near you', 'status': "NOT FOUND"}
        return msg


@shared_task(bind=True)
def updateScheduleRideExpiration(self, *args, **kwargs):
    print("coming to expiration function and booking id is ==>",
          kwargs['booking_id'])
    if ScheduledOrder.objects.filter(booking_id=kwargs['booking_id'], booking__status_id=1).exists():
        BookingDetail.objects.filter(id=kwargs['booking_id']).update(
            status_id=13
        )


@shared_task(bind=True)
def call_api_task(self):
    response = VehicleTypes.objects.all()

    result = []
    for item in response:
        result.append(item.id)
    return result


@shared_task(bind=True)
def test_fun(self):

    print("count of user feedback ==>", UserFeedback.objects.all().values())
    # UserFeedback.objects.all().delete()
    # UserFeedback.objects.create(id=3)

    return "created"


@shared_task(bind=True)
def UpdateSubscriptionStatus(self, *args, **kwargs):
    Vehicle_Subscription.objects.filter(
        id=kwargs['vehcile_subscription_id']).update(status='Expired', is_expired=True)

    return "status updated successfully"

# @shared_task(bind=True)
# def UpdateDriverSearchResult(self, *args, **kwargs):
#     # booking_obj = BookingDetail.objects.get(id=kwargs['booking_id'])


#     return "status updated successfully"


@shared_task(bind=True)
def AssignDrivertoUser(self, *args, **kwargs):

    print("session booking id", args, kwargs)
    booking_id = args[0]

    if Driver.objects.filter(vehicle__vehicletypes_id=kwargs['vehicle_type_id'], is_online=True, driver_status='Validated'):

        driver_obj_location = Driver.objects.filter(
            vehicle__vehicletypes_id=kwargs['vehicle_type_id'], is_online=True).values()

        finalArr = []
        final_obj = {}

        randomly_assigning_driver = []

        if type(kwargs['location_details']) == dict:
            start_location = (kwargs['location_details']['start_location']
                              ['lat'], kwargs['location_details']['start_location']['lng'])
        else:
            start_location = (kwargs['location_details'][0]['start_location']
                              ['lat'], kwargs['location_details'][0]['start_location']['lng'])

        for i in driver_obj_location:
            print("i---------->>>>>---->>>>", i)
            end_location = (i['live_lattitude'], i['live_longitude'])

            final_obj['lat'] = i['live_lattitude']
            final_obj['lng'] = i['live_longitude']
            final_obj['total_km'] = geopy.distance.geodesic(
                start_location, end_location).km
            final_obj['driver_id'] = i['user_id']
            finalArr.append(final_obj)
            final_obj = {}

            if BookingDetail.objects.filter(Q(driver_id=i['user_id']) & (Q(status_id=1) | Q(status_id=2) | Q(status_id=6) | Q(status_id=8) | Q(status_id=9) | Q(status_id=10))):
                print("dont assign", i['user_id'])
                for j in finalArr:
                    if j.get('driver_id') == i['user_id']:
                        finalArr.remove(j)
                        break
            else:
                min_km = min(finalArr, key=lambda x: x['total_km'])
                randomly_assigning_driver.append(min_km)

            if (randomly_assigning_driver == [] or len(randomly_assigning_driver) == 0):
                print("all vehicles are busy")
                return 'all vehicles are busy in state please try after some time'

            else:

                driver_obj = CustomUser.objects.get(
                    id=randomly_assigning_driver[-1]['driver_id'])

                html_template = 'orderTemplate.html'
                context = {'driver_name': driver_obj.first_name,
                           'driver_mobile_number': driver_obj.mobile_number, 'user_name': kwargs['username']}
                email_html_template = get_template(
                    html_template).render(context)
                email = EmailMessage('Order Notification From Logistics',
                                     email_html_template,
                                     from_email='logisticscom70@gmail.com',
                                     to=[kwargs['user_email']]
                                     )
                email.content_subtype = "html"
                email.send(fail_silently=False)

                # send_mail(
                #     'Order Notification From Logistics',
                #     'Hey '+kwargs['username']+' your order has been started\n please reach out the driver '+driver_obj.first_name+' Ph +'+driver_obj.mobile_number,
                #     'logisticscom70@gmail.com',
                #     [kwargs['user_email']],
                #     fail_silently=False,
                # )

                print("assigned driver successfully")
                booking_obj = BookingDetail.objects.filter(id=kwargs['booking_id']).update(
                    driver_id=randomly_assigning_driver[-1]['driver_id'])
                return 'driver assigned successfully'
        print("second driver assigned")
        return 'driver assigned successfully'
    else:
        print("no driver found")
        return 'no drivers found at the movement'


@shared_task(bind=True)
def getDriverDetailsByID(self, user_id):
    driver_obj = Driver.objects.filter(user_id=user_id).values('id', 'vehicle_id', 'vehicle__vehicle_status', 'vehicle__vehicle_name', 'vehicle__vehicle_number', 'driver_driving_license', 'user__first_name', 'badge', 'user__adhar_card_front_side_img_path', 'user__adhar_card_back_side_img_path', 'user__role__user_role_name', 'user__mobile_number', 'vehicle__permit_front_side_img_path', 'vehicle__registration_certificate_front_side_img_path', 'vehicle__registration_certificate_back_side_img_path', 'vehicle__pollution_certificate_front_side_img_path',
                                                               'license_img_front', 'license_img_back', 'insurence_img', 'passbook_img', 'user_id', 'owner_id', 'fitness_certificate_back_side_img_path', 'fitness_certificate_front_side_img_path', 'license_expire_date', 'insurance_expire_date', 'fitness_certificate_expire_date', 'vehicle__permit_expire_date', 'vehicle__rc_expire_date', 'vehicle__emission_certificate_expire_date', 'vehicle__vehicletypes__vehicle_type_name', 'vehicle__vehicletypes__id', 'vehicle__vehicletypes__vehicle_type_image', 'user__profile_image', 'vehicle__is_active', 'driver_status')

    driver_image_obj_img = Driver.objects.get(user_id=user_id)
    live_url = "https://logistics.thestorywallcafe.com/media"

    imagesDict = {
        "license_img_front": base64.b64encode(requests.get(live_url + str(driver_image_obj_img.license_img_front)).content),
        "license_img_back": base64.b64encode(requests.get(live_url + str(driver_image_obj_img.license_img_back)).content),
        "passbook_img": base64.b64encode(requests.get(live_url + str(driver_image_obj_img.passbook_img)).content)
    }

    if driver_obj[0]['owner_id'] == user_id:
        obj_with_owner_details = list(driver_obj)
        if obj_with_owner_details[0]['user__profile_image'] == "":
            obj_with_owner_details[0]['user__profile_image'] = None
        obj_with_owner_details[0]['owner_details'] = None
        vehcile_id = driver_image_obj_img.vehicle_id

        # print("vehcile_id===> vehcile_id===> with subscription", vehcile_id, Vehicle_Subscription.objects.filter(vehicle_id_id=vehcile_id).last())

        if Vehicle_Subscription.objects.filter(vehicle_id_id=vehcile_id).last():
            obj_with_owner_details[0]['is_subscribed'] = True
        else:
            obj_with_owner_details[0]['is_subscribed'] = False

        final_value = {'data': obj_with_owner_details,
                       'base64ImageData': imagesDict}

        return final_value
    else:
        # print("printing in else block")

        obj_with_owner_details = list(driver_obj)
        print("obj_with_owner_details==>>>", obj_with_owner_details)
        if obj_with_owner_details[0]['user__profile_image'] == "":
            obj_with_owner_details[0]['user__profile_image'] = None

        owner_details = CustomUser.objects.filter(
            id=driver_obj[0]['owner_id']).values().first()

        # print("query==>", Driver.objects.filter(owner_id=driver_obj[0]['owner_id']).values('driver_driving_license'))

        owner_licence_number = Driver.objects.filter(
            owner_id=driver_obj[0]['owner_id']).values('owner_driving_licence').first()
        owner_licence_number = owner_licence_number['owner_driving_licence']

        if owner_licence_number is not None:
            owner_details['driver_driving_license'] = owner_licence_number

        vehcile_id = driver_image_obj_img.vehicle_id
        if Vehicle_Subscription.objects.filter(vehicle_id_id=vehcile_id).last():
            obj_with_owner_details[0]['is_subscribed'] = True
        else:
            obj_with_owner_details[0]['is_subscribed'] = False

        # if Driver.objects.filter(Q(owner_id=None)):
        #     obj_with_owner_details[0]['owner_details'] = None
        # else:
        if Driver.objects.get(user_id=user_id).owner_id is None:
            obj_with_owner_details[0]['owner_details'] = None
        else:
            obj_with_owner_details[0]['owner_details'] = [owner_details]

        final_value = {'data': obj_with_owner_details,
                       'base64ImageData': imagesDict}

        return final_value


@shared_task
def export_database_task():

    print("excuted")
    try:
        # Call the Django management command to export the database
        call_command(
            'dumpdata', '--output=/logistics/database/logistics_db.json')
        # You can replace 'database_dump.json' with your desired file name and path.
    except Exception as e:
        # Handle any exceptions that might occur during the export process
        # For example, you can log the error or send a notification.
        pass
