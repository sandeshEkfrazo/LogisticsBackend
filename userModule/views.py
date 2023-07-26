from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from logisticsapp.models import *
from rest_framework.response import Response
import datetime
from django.db.models import Q
import geopy.distance
import sys
from rest_framework import status
import random
import http.client
import json
from django_celery_beat.models import ClockedSchedule, CrontabSchedule, PeriodicTask
from logisticsapp import views
from datetime import datetime

coords_1 = (52.2296756, 21.0122287)
coords_2 = (52.406374, 16.9251681)

# print(geopy.distance.geodesic(coords_1, coords_2).km)


class DeleteTasks(APIView):
    def get(self, request):
        ClockedSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()

        return Response("deleted")


# Create your views here.

class BillingRequestApi(APIView):
    def post(self, request):
        data = request.data
        is_bill_required = data['is_bill_required']
        is_bill_recived = data['is_bill_recived']
        order_id = data['order_id']
        
        if is_bill_recived is None:
            BookingDetail.objects.filter(order=order_id).update(is_bill_required=is_bill_required)
            return Response({'message': 'bill accepted successfully'})
        if is_bill_required is None:
            BookingDetail.objects.filter(order=order_id).update(is_bill_recived=is_bill_recived)
            return Response({'message': 'bill recived successfully'})

def getMinDistancefromuserToDriver(finalArr):
    min_km = min(finalArr, key=lambda x:x['total_km'])
    return min_km


####################################
# from datetime import datetime

# bk = BookingDetail.objects.get(id=1).ordered_time
# print("bk==>", str(bk).split()[1])
# time = str(bk).split()[1]
# print(str(time).split("+")[0].split(':')[0], str(time).split("+")[0])

# start_time = str(time).split("+")[0].split(':')
# end_time = str(time).split("+")[0].split(':')

# t1 = datetime.strptime(start_time[0]+":"+start_time[1]+":"+str(00), "%H:%M:%S")
# print('Start time:', t1.time())

# t2 = datetime.strptime(start_time[0]+":"+start_time[1]+":"+str(00), "%H:%M:%S")
# print('End time:', t2.time())

# delta = t2 - t1
# print("delta==>", delta)

#############################

from dateutil import parser

s = parser.isoparse("2023-03-10T07:58:10.585622Z")
# print("s==>", s)

from datetime import timedelta
from django.shortcuts import render

def renderTemplate(request):
    return render(request, 'orderTemplate.html')
# import datetime
# from datetime import timedelta
# from dateutil import parser

class BookVehicleAPI(APIView):
    def get(self, request, order_id, user_id):
        order_detail = BookingDetail.objects.filter(order_id=order_id, order__user_id=user_id).values(
            'driver_id', 'status','status__status_name', 'order__vehicle_number', 'driver__first_name', 
            'driver__mobile_number', 'status__status_name', 'order__otp', 'driver__vehicle__vehicle_name',
            'order__total_estimated_cost', 'order__location_detail', 'request_cancel',
            'driver__profile_image_path', 'driver__vehicle__vehicletypes__vehicle_type_image',
            'driver__driver_id__rating', 'travel_details'
            )
    
        final_order_detail = list(order_detail)
        
        for i in list(final_order_detail):
            vehicle_type = Driver.objects.filter(user_id=i['driver_id']).values('vehicle__vehicletypes_id')

            driver_rating = UserFeedback.objects.filter(user_id = i['driver_id']).values('rating')
            # print("driver_rating==>>", driver_rating)
            # if rating == None:
            #     rating=5
            #     return Response({'data':order_detail,'rating':rating}) 
            
            # i['driver_rating'] = driver_rating

            if i['driver__profile_image_path'] == "":
                i['driver__profile_image_path'] = None
            i['vehicle_type_id'] = vehicle_type[0]['vehicle__vehicletypes_id']
        return Response({'data': final_order_detail})


    def post(self, request):
        data = request.data

        location_detail = data['location_details']
        vehicle_number = data['vehicle_number']
        user_id = data['user_id']
        travel_details = data['travel_details']
        sub_user_ph_number=data['sub_user_ph_number']
        is_scheduled = data['is_scheduled']

        if data['vehicle_number'] is not None:
            vehicle_obj = Vehicle.objects.get(vehicle_number=data['vehicle_number'])

            get_est_cost = views.find_vehicle_estimation_cost(data, vehicle_obj.vehicletypes_id, location_detail)

            # print("get_est_cost by vehicle number book by number ==>>", get_est_cost)

            order_obj = OrderDetails.objects.create(user_id=user_id, vehicle_number=vehicle_number, location_detail=location_detail,total_estimated_cost = get_est_cost['total_fare_amount'])

            total_amount_without_actual_time_taken = get_est_cost['final_km_charge'] + get_est_cost['base_fee']

            driver_obj = Driver.objects.get(vehicle__vehicle_number=vehicle_number)

            booking_obj = BookingDetail.objects.create(order_id=order_obj.id, driver_id=driver_obj.user_id, status_id=1, travel_details=travel_details, ordered_time=datetime.datetime.now(), sub_user_phone_numbers=sub_user_ph_number, total_amount_without_actual_time_taken=total_amount_without_actual_time_taken)

            return Response({'message': 'wait till the driver accepts your order', 'order_id':order_obj.id,'user':sub_user_ph_number, 'vehicle_type_id': vehicle_obj.vehicletypes_id})
        else:
            
            if data['schedule'] is not None:

                print("scheduled data==>>>>>", data['schedule'])


                order_obj = OrderDetails.objects.create(user_id=user_id, location_detail=location_detail, total_estimated_cost=data['total_estimated_cost'])

                get_est_cost = views.find_vehicle_estimation_cost(data, data['vehicle_type'], location_detail)

                total_amount_without_actual_time_taken = get_est_cost['final_km_charge'] + get_est_cost['base_fee']

                booking_obj = BookingDetail.objects.create(order_id=order_obj.id, status_id=1, travel_details=travel_details, ordered_time=datetime.datetime.now(), sub_user_phone_numbers=sub_user_ph_number,total_amount_without_actual_time_taken=total_amount_without_actual_time_taken, is_scheduled=is_scheduled)

                
                dt = parser.isoparse(data['schedule']['scheduled_datetime'])

                last_hour_date_time = dt - timedelta(hours = 1)

                clocked_obj = ClockedSchedule.objects.create(
                    clocked_time = last_hour_date_time
                )

                user_email = CustomUser.objects.get(id=user_id)

                task_start = PeriodicTask.objects.create(name="scheduleForAssignDriver"+str(clocked_obj.id), task="userModule.tasks.AssignDrivertoUser",clocked_id=clocked_obj.id, one_off=True, args=json.dumps([int(booking_obj.id)],), kwargs=json.dumps({'booking_id': booking_obj.id, 'vehicle_type_id': data['vehicle_type'], 'user_email': user_email.email, 'username': user_email.first_name, 'location_details': location_detail}))

                ScheduledOrder.objects.create(booking_id=booking_obj.id, scheduled_date_and_time=data['schedule']['scheduled_datetime'], periodic_task_id=task_start.id)

                request.session['user_booking_id'] = booking_obj.id

                return Response({'message': 'order scheduled successfully'})

            
            # below query checking the type of the vehicle of particular driver along with he is online or not.
            print("first=>",Driver.objects.filter(vehicle__vehicletypes_id=data['vehicle_type'], is_online=True))
            print("second=>", Driver.objects.filter(vehicle__vehicletypes_id=data['vehicle_type']))
            print("third==>", Driver.objects.filter(is_online=True))
            
            if Driver.objects.filter(vehicle__vehicletypes_id=data['vehicle_type'], is_online=True):
                
                driver_obj_location = Driver.objects.filter(vehicle__vehicletypes_id=data['vehicle_type'], is_online=True).values()

                

                finalArr = []
                final_obj = {}

                randomly_assigning_driver = []

                if type(location_detail) == dict:
                    start_location = (location_detail['start_location']['lat'], location_detail['start_location']['lng'])
                else:
                    start_location = (location_detail[0]['start_location']['lat'], location_detail[0]['start_location']['lng'])
                    
                for i in driver_obj_location:
                    # print("i---------->>>>>---->>>>", i)
                    end_location = (i['live_lattitude'], i['live_longitude'])
                    
                    final_obj['lat'] = i['live_lattitude']
                    final_obj['lng'] = i['live_longitude']
                    final_obj['total_km'] = geopy.distance.geodesic(start_location, end_location).km
                    final_obj['driver_id'] = i['user_id']
                    finalArr.append(final_obj)
                    final_obj = {}

                    # print("i==>", i['live_lattitude'], i['live_longitude'])

                    # print("total km==>",geopy.distance.geodesic(start_location, end_location).km)
                    # print("finalArr=========>>>>--->>", finalArr)
                    if BookingDetail.objects.filter(Q(driver_id=i['user_id']) & (Q(status_id=1) | Q(status_id=2) | Q(status_id=6) | Q(status_id=8) | Q(status_id=9) | Q(status_id=10))):
                        # print("dont assign", i['user_id'])
                        for j in finalArr:
                            if j.get('driver_id') == i['user_id']:
                                finalArr.remove(j)
                                break
                    else:
                        min_km = min(finalArr, key=lambda x:x['total_km'])
                        randomly_assigning_driver.append(min_km)


                # print("randomly_assigning_driver", randomly_assigning_driver)

                if (randomly_assigning_driver == [] or len(randomly_assigning_driver) == 0):
                    return Response({'err': "all vehicles are busy in state please try after some time", 'status': 'ALREADY RESERVED'},status=status.HTTP_306_RESERVED)
                else:
                    order_obj = OrderDetails.objects.create(user_id=user_id, location_detail=location_detail, total_estimated_cost=data['total_estimated_cost'])

                    get_est_cost = views.find_vehicle_estimation_cost(data, data['vehicle_type'], location_detail)

                    # print("get_est_cost by vehicle number random vehicle ==>>", get_est_cost)

                    total_amount_without_actual_time_taken = get_est_cost['final_km_charge'] + get_est_cost['base_fee']


                    booking_obj = BookingDetail.objects.create(order_id=order_obj.id, driver_id=randomly_assigning_driver[-1]['driver_id'], status_id=1, travel_details=travel_details, ordered_time=datetime.datetime.now(), sub_user_phone_numbers=sub_user_ph_number,total_amount_without_actual_time_taken=total_amount_without_actual_time_taken, is_scheduled=is_scheduled)

                    return Response({'message': 'wait till the driver accepts your order', 'data': finalArr, 'order_id':order_obj.id})
            return Response({'message': 'no vehicle found near you', 'status': "NOT FOUND"}, status=status.HTTP_404_NOT_FOUND)

class CancelOrderByUser(APIView):
    def get(self, request, order_id):

        BookingDetail.objects.filter(order_id=order_id).update(status=5)
        
        return Response({'message': 'your order has been canceled'})

    def post(self, request):
        order_detail = BookingDetail.objects.filter(order__user_id=request.data['user_id']).order_by('-id').values('order_id','driver_id', 'status','status__status_name', 'order__vehicle_number', 'driver__first_name', 'driver__mobile_number', 'status__status_name', 'order__otp', 'driver__vehicle__vehicle_name', 'order__total_estimated_cost', 'order__location_detail', 'request_cancel', 'travel_details', 'ordered_time', 'pickedup_time', 'order_accepted_time', 'canceled_time', 'order_droped_time')
        return Response({'data': order_detail})

class UserFeedBackApi(APIView):
    def post(self, request):
        data = request.data

        order_id = data['order_id']
        user_id = data['user_id']
        driver_id = data['driver_id']
        review = data['review']
        ratings = data['ratings']
        rating_given_by = data['rating_given_by']

        UserFeedback.objects.create(
            driver_id= driver_id,
            user_id = user_id,
            rating = ratings,
            order_id = order_id,
            rating_given_by = rating_given_by
        )

        return Response({'message': 'user feedback updated successfully'})


class UserAndDriverrecipt(APIView):
    def post(self, request):
        data = request.data

        if data['user_id'] is not None:
            order_obj = OrderDetails.objects.get(user_id=data['user_id'], id=data['order_id'])

            vehicle_obj = Vehicle.objects.get(vehicle_number=order_obj.vehicle_number)

            vehicle_type_id = vehicle_obj.vehicletypes_id

            vehicle_type_obj = VehicleTypes.objects.get(id=vehicle_type_id)

            total_price = float(order_obj.total_estimated_cost) + float(vehicle_type_obj.min_charge) 

            final_output = {
                "trip_charges": order_obj.total_estimated_cost,
                "GST": "",
                "booking_fee": vehicle_type_obj.min_charge,
                "total_price": total_price
            }

            return Response({'message': 'recipt details', "data": final_output})
        
        if data['driver_id'] is not None:
            booking_obj = BookingDetail.objects.get(driver_id=data['driver_id'], order_id=data['order_id'])

            order_obj = OrderDetails.objects.filter(id=booking_obj.order_id).last()

            vehicle_obj = Vehicle.objects.get(vehicle_number=order_obj.vehicle_number)

            vehicle_type_id = vehicle_obj.vehicletypes_id

            vehicle_type_obj = VehicleTypes.objects.get(id=vehicle_type_id)

            total_price = float(order_obj.total_estimated_cost) + float(vehicle_type_obj.min_charge) 

            final_output = {
                "trip_charges": order_obj.total_estimated_cost,
                "GST": "",
                "booking_fee": vehicle_type_obj.min_charge,
                "total_price": total_price
            }

            return Response({'message': 'recipt details', "data": final_output})


# print("BookingDetail.objects.get(order_id=order_id).order_accepted_time==>", BookingDetail.objects.get(order_id=786).order_accepted_time, str(BookingDetail.objects.get(order_id=786).order_accepted_time).split('+')[0])

class DriverDocumentExpiryDate(APIView):
    def post(self, request):
        licence_exp_date = request.data['licence_exp_date']
        permit_exp_date = request.data['permit_exp_date']
        fitness_exp_date = request.data['fitness_exp_date']
        pollution_exp_date = request.data['pollution_exp_date']
        insurance_exp_date = request.data['insurance_exp_date']
        reg_cer_exp_date  = request.data['reg_cer_exp_date']
        driver_id = request.data['driver_id']
        vehicle_id = Driver.objects.get(user_id=driver_id).vehicle_id
    	

        Driver.objects.filter(user_id=driver_id).update(
            license_expire_date = licence_exp_date, 
            fitness_certificate_expire_date = fitness_exp_date, 
            insurence_expire_date = insurance_exp_date
        )
        Vehicle.objects.filter(id=vehicle_id).update(
		permit_expire_date = permit_exp_date, 
	 	emission_test_expire_date = pollution_exp_date, 
	 	rc_expire_date = reg_cer_exp_date
	)     
        
		

        return Response({'message': 'expiry date updated successfully'})

import requests

def sendMessage():
    url = "https://control.msg91.com/api/v5/flow/"

    payload = {
        "template_id": "617ba900d6fc0544582a4dda",
        "sender": "ARCDEX",
        "short_url": "1 (On) or 0 (Off)",
        "mobiles": "918971290497",
        "var": "hello how are you",
        "VAR2": "hello how are you"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authkey": "351156AJtRgBbz5ff5687cP1"
    }

    response = requests.post(url, json=payload, headers=headers)

    # print("response text from send sms =>",response.text)


def resendOTP(mobile_number):
    conn = http.client.HTTPSConnection("api.msg91.com")

    conn.request("GET", "/api/v5/otp/retry?authkey=351156AJtRgBbz5ff5687cP1&retrytype=retry&mobile="+str(mobile_number))

    res = conn.getresponse()
    data = res.read()

    # print(data.decode("utf-8"))
    return data.decode("utf-8")

def sendMobileOTp(mobile_number):
    
    conn = http.client.HTTPSConnection("api.msg91.com")

    payload = "{\n  \"Param1\": \"value1\",\n  \"Param2\": \"value2\",\n  \"Param3\": \"value3\"\n}"

    headers = { 'Content-Type': "application/JSON" }

    conn.request("GET", "/api/v5/otp?template_id=617bfb6191cb292c2c0b1b74&mobile="+str(mobile_number)+"&authkey=351156AJtRgBbz5ff5687cP1", payload, headers)

    res = conn.getresponse()
    data = res.read()

    # print(data.decode("utf-8"))
    return data.decode("utf-8")


def verifyOTP(mobile_number, otp):
    conn = http.client.HTTPSConnection("api.msg91.com")

    conn.request("GET", "/api/v5/otp/verify?otp="+str(otp)+"&authkey=351156AJtRgBbz5ff5687cP1&mobile="+str(mobile_number))

    res = conn.getresponse()
    data = res.read()

    # print("verifying otp response ====>>",data)

    return data.decode("utf-8")

class ResendOTP(APIView):
    def post(self,request):
        res = resendOTP(request.data['mobile_number'])
        return Response(res)

class getUserPhoneNumber(APIView):
    def get(self, request, order_id):
        booking_obj = BookingDetail.objects.get(order_id=order_id)

        return Response({
            'sub_user_phone_number': booking_obj.sub_user_phone_numbers
        })


    def post(self, request):
        phone_number = request.data['phone_number']

        sendMobileOTp(phone_number)
        return Response({'message': 'otp send successfully'})

    def put(self, request):
        phone_number = request.data['phone_number']
        otp = request.data['otp']

        verified_otp = verifyOTP(phone_number, otp)
        # print('verified otp', verified_otp)

        # if json.loads(verified_otp)['type'] = 'error':
        #     return Response(json.loads(verified_otp), status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(json.loads(verified_otp))
        

class TotalAmountAfterRideComplete(APIView):
    def post(self, request):
        data = request.data

        vehicle_type_id = data['vehicle_type_id']
        order_id = data['order_id']
        user_id = data['user_id']

        if user_id is not None:
            booking_obj = BookingDetail.objects.get(order_id=order_id, order__user_id=data['user_id'])
      
        booking_obj = BookingDetail.objects.get(order_id=order_id)

        vehicle_obj = VehicleTypes.objects.get(id=vehicle_type_id)

        per_min_price = vehicle_obj.per_min_price


        actual_time_taken = str(booking_obj.actual_time_taken_to_complete).split(':')
        if actual_time_taken[0] == '00':
            actual_amount_for_time_ = (int(actual_time_taken[1]) * float(per_min_price)) + booking_obj.total_amount_without_actual_time_taken
            booking_obj = BookingDetail.objects.filter(order_id=order_id).update(total_amount=actual_amount_for_time_)
        else:
            actual_amount_for_time_ =(((int(actual_time_taken[0]) * 60) + int(actual_time_taken[1])) * float(per_min_price)) + booking_obj.total_amount_without_actual_time_taken
            booking_obj = BookingDetail.objects.filter(order_id=order_id).update(total_amount=actual_amount_for_time_)

        return Response({'message': 'data updated', 'total_amount': format(actual_amount_for_time_, '.2f') })


from .tasks import *

from django.http import HttpResponse

# Create your views here.
def hello(request):
    test_fun.delay()
    # test_fun()
    return HttpResponse("<center><h1>hello world</h1></center>")

#from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist   
class AllScheduledOrder(APIView):
    def get(self, request):      

        print("insdie get")


        scheduled_order_obj = ScheduledOrder.objects.all().values(
            'booking__order__user__first_name', 'booking__order__location_detail', 'booking__order_id', 'booking__total_amount', 'booking__travel_details', 'booking__ordered_time', 'booking__driver__first_name', 'booking__driver_id', 'scheduled_date_and_time', 'booking__order__user__mobile_number', 'booking__order__total_estimated_cost', 'booking__status_id', 'booking__sub_user_phone_numbers', 'booking__order__user_id', 'booking__status__status_name', 'booking__status_id', 'booking__driver__vehicle__vehicle_number', 'booking__driver__mobile_number', 'booking__driver__vehicle__vehicletypes__vehicle_type_name'
        ).order_by('-id')

        if request.query_params.get('order_id'):
            shedule_obj_with_driver_order = ScheduledOrder.objects.filter(Q(booking__order_id=request.query_params.get('order_id')) & Q(booking__driver_id=request.query_params['driver_id'])).values(
                'booking__order__user__first_name', 'booking__order__location_detail', 'booking__order_id', 'booking__total_amount', 'booking__travel_details', 'booking__ordered_time', 'booking__driver__first_name', 'booking__driver_id', 'scheduled_date_and_time', 'booking__order__user__mobile_number', 'booking__order__total_estimated_cost', 'booking__status_id', 'booking__sub_user_phone_numbers', 'booking__order__user_id', 'booking__status__status_name', 'booking__status_id', 'booking__driver__vehicle__vehicle_number', 'booking__driver__mobile_number', 'booking__driver__vehicle__vehicletypes__vehicle_type_name'
            ).last()
            if type(shedule_obj_with_driver_order['booking__order__location_detail']) == dict:
                start_location = (shedule_obj_with_driver_order['booking__order__location_detail']['start_location']['lat'], shedule_obj_with_driver_order['booking__order__location_detail']['start_location']['lng'])
            else:
                start_location = (shedule_obj_with_driver_order['booking__order__location_detail']['start_location']['lat'], shedule_obj_with_driver_order['booking__order__location_detail']['start_location']['lng'])
            
            driver_obj = Driver.objects.get(user_id=request.query_params['driver_id'])

            end_location = (driver_obj.live_lattitude , driver_obj.live_longitude)

            total_km = geopy.distance.geodesic(start_location, end_location).km

            shedule_obj_with_driver_order['distance'] = round(total_km, 1)

            print("rtru 1")

            return Response({'data': shedule_obj_with_driver_order})


        if request.query_params:

            print("coming inside requst paramas")
            
            driver_o = Driver.objects.get(user_id=request.query_params['driver_id'])
            vehcile_id = driver_o.vehicle_id

            if Driver.objects.filter(Q(user_id=request.query_params['driver_id']) & Q(driver_status="Validated")) and Vehicle_Subscription.objects.filter(vehicle_id_id=vehcile_id).exists():

                if ScheduledOrder.objects.filter(Q(booking__driver_id=request.query_params['driver_id']) & ~Q(Q(booking__status_id=6) | Q(booking__status_id=5) | ~Q(booking__status_id=2))):


                    driver_obj = Driver.objects.get(user_id=request.query_params['driver_id'])

                    
                    booking_details = ScheduledOrder.objects.filter(Q(booking__driver_id=request.query_params['driver_id']) & Q(booking__status_id=2)).values('booking__order__user__first_name', 'booking__order__location_detail', 'booking__order_id', 'booking__total_amount', 'booking__travel_details', 'booking__ordered_time', 'booking__driver__first_name', 'booking__driver_id', 'scheduled_date_and_time', 'booking__order__user__mobile_number', 'booking__order__total_estimated_cost', 'booking__status_id','booking__sub_user_phone_numbers', 'booking__order__user_id', 'booking__status__status_name', 'booking__status_id', 'booking__driver__vehicle__vehicle_number', 'booking__driver__mobile_number', 'booking__driver__vehicle__vehicletypes__vehicle_type_name').last()
                    
                    
                    if type(booking_details['booking__order__location_detail']) == dict:
                        start_location = (booking_details['booking__order__location_detail']['start_location']['lat'], booking_details['booking__order__location_detail']['start_location']['lng'])
                    else:
                        start_location = (booking_details['booking__order__location_detail'][0]['start_location']['lat'], booking_details['booking__order__location_detail'][0]['start_location']['lng'])

                    end_location = (driver_obj.live_lattitude , driver_obj.live_longitude)

                    total_km = geopy.distance.geodesic(start_location, end_location).km

                    booking_details['distance'] = round(total_km, 1)

                    booking_status = BookingDetail.objects.filter(driver_id=request.query_params['driver_id']).values().last()

                    return Response({'data': [booking_details], 'message': 'you have already selected the order', "booking__status_id": booking_details['booking__status_id']})
                    # return Response("hello")
        

                else:
                    shedule_orders_with_no_drivers = ScheduledOrder.objects.filter(Q(booking__driver_id=None) & Q(booking__is_scheduled=True)).values('booking__order__user__first_name', 'booking__order__location_detail', 'booking__order_id', 'booking__total_amount', 'booking__travel_details', 'booking__ordered_time', 'booking__driver__first_name', 'booking__driver_id', 'scheduled_date_and_time', 'booking__order__user__mobile_number', 'booking__order__total_estimated_cost', 'booking__status_id', 'booking__sub_user_phone_numbers', 'booking__order__user_id', 'booking__status__status_name', 'booking__status_id', 'booking__driver__vehicle__vehicle_number', 'booking__driver__mobile_number', 'booking__driver__vehicle__vehicletypes__vehicle_type_name')
                    
                    return Response({'data': shedule_orders_with_no_drivers, "booking__status_id": 1})

                

                final_arr = list(scheduled_order_obj)
                for i in final_arr:
                    if type(i['booking__order__location_detail']) == dict:
                        start_location = (i['booking__order__location_detail']['start_location']['lat'], i['booking__order__location_detail']['start_location']['lng'])
                    else:
                        start_location = (i['booking__order__location_detail'][0]['start_location']['lat'], i['booking__order__location_detail'][0]['start_location']['lng'])

                    end_location = (driver_obj.live_lattitude , driver_obj.live_longitude)

                    total_km = geopy.distance.geodesic(start_location, end_location).km

                    # print("total km b/w driver and strt location", total_km)

                    # print(final_arr)
                    i['distance'] = round(total_km, 1)
                    i['booking__order__total_estimated_cost'] = round(i['booking__order__total_estimated_cost'], 2)

                    if i['booking__driver_id'] == None:
                        finalArr.append(i)

                

                return Response({"data":finalArr})
            else:
                return Response({"message":"wait till the verification", 'data': []})
        else:
            return Response({"data":scheduled_order_obj})

            

    def post(self, request):
        driver_id = request.data['driver_id']
        order_id = request.data['order_id']

        if BookingDetail.objects.filter(Q(driver_id=driver_id) & (Q(status_id=2) | Q(status_id=6))).exists():
            return Response({'error': 'Already Driver has accepted other order please select different driver.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        BookingDetail.objects.filter(order_id=order_id).update(driver_id=driver_id, status_id=2)

        return Response({'message': 'you have selected the order successfully', 'order_id': "order_id"})


from django.http import JsonResponse
class CallAPI(APIView):
    def get(self, request):
        result = call_api_task.delay()
        data = result.get()
        return JsonResponse(data, safe=False)


class DriverWithDistanceAPI(APIView):
    def get(self, request):
        order_id = request.query_params['order_id']

        order_obj = OrderDetails.objects.get(id=order_id)

        all_driver_obj = Driver.objects.filter(driver_status="Validated").values('user_id', 'user__first_name', 'live_lattitude', 'live_longitude')


        finalArr = []
        for i in list(all_driver_obj):
            if BookingDetail.objects.filter(Q(driver_id=i['user_id']) & (Q(status_id=1) | Q(status_id=2) | Q(status_id=6) | Q(status_id=8) | Q(status_id=9) | Q(status_id=10))):
                pass
            else:
                if i['live_lattitude'] is not None or i['live_longitude'] is not None:

                    if type(order_obj.location_detail) == dict:
                        start_location = (order_obj.location_detail['start_location']['lat'], order_obj.location_detail['start_location']['lng'])
                    else:
                        start_location = (order_obj.location_detail[0]['start_location']['lat'], order_obj.location_detail[0]['start_location']['lng'])

                    end_location = (i['live_lattitude'] , i['live_longitude'])

                    total_km = geopy.distance.geodesic(start_location, end_location).km

                    i['distance'] = str(round(total_km, 1)) + " km"

                    finalArr.append(i)
                else:
                    i['distance'] = None

            return Response(finalArr)
