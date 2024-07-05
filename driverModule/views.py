from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from userModule.models import *
import random
from logisticsapp.models import *
from rest_framework import status
from django.db.models import Q
import geopy.distance
from userModule.views import *
import datetime
from account.auth import *
from django.utils.decorators import method_decorator

coords_1 = (52.2296756, 21.0122287)
coords_2 = (52.406374, 16.9251681)

# print("total km",geopy.distance.geodesic(coords_1, coords_2).km)

# import subprocess
# # current_machine_id = subprocess.check_output('wmic bios get serialnumber').split('\n')[1].strip()
# print(subprocess.check_output('wmic bios get serialnumber').decode("utf-8"))

from datetime import timedelta
from django.utils import timezone
# Create your views here.
def estimationCostCalculation(order_id, update_status):
    vehicle_price_per_km = BookingDetail.objects.filter(order_id=order_id).values('driver__vehicle__vehicletypes__per_km_price', 'order__location_detail')

    total_km = []
    price_per_km = []

    for i in vehicle_price_per_km:
        # Append the per kilometer price
        price_per_km.append(float(i['driver__vehicle__vehicletypes__per_km_price']))
        
        # Handle location details
        if type(i['order__location_detail']) is not dict:
            for k in i['order__location_detail']:
                distance_text = k['distance']['text']
                if 'km' in distance_text:
                    total_km.append(float(distance_text.replace('km', '').strip()))
                elif 'm' in distance_text:
                    total_km.append(float(distance_text.replace('m', '').strip()) / 1000)
        else:
            distance_text = i['order__location_detail']['distance']['text']
            if 'km' in distance_text:
                total_km.append(float(distance_text.replace('km', '').strip()))
            elif 'm' in distance_text:
                total_km.append(float(distance_text.replace('m', '').strip()) / 1000)
    if price_per_km:
        price_per_km_value = price_per_km[0]
    else:
        price_per_km_value = 0  # or some other default value

    # Calculate total estimated cost
    total_estimated_cost = price_per_km[0] * sum(total_km)

    # Update BookingDetail with status and total amount
    BookingDetail.objects.filter(order_id=order_id).update(status=update_status)

    return total_estimated_cost
# def estimationCostCalculation(order_id, update_status):
# 	vehicle_price_per_km = BookingDetail.objects.filter(order_id=order_id).values('driver__vehicle__vehicletypes__per_km_price', 'order__location_detail')

# 	total_km = []
# 	price_per_km = []

	

# 	for i in vehicle_price_per_km:
# 		# print("i==>>", i)
# 		price_per_km.append(float(i['driver__vehicle__vehicletypes__per_km_price']))
# 		# print("i['order__location_detail']==>", i['order__location_detail'], 'type==>', type(i['order__location_detail']))
# 		if type(i['order__location_detail']) is not dict:
# 			for k in i['order__location_detail']:
# 				total_km.append(float(k['distance']['text'].replace('km', '')))                    
# 		else:
# 			total_km.append(float(i['order__location_detail']['distance']['text'].replace('km', '')))
			

# 	# print("total_km=>", total_km, sum(total_km))

# 	total_estimated_cost = price_per_km[0] * sum(total_km)

# 	# OrderDetails.objects.filter(id=order_id).update(total_estimated_cost=total_estimated_cost)
# 	# BookingDetail.objects.filter(order_id=order_id).update(status=update_status, total_amount=total_estimated_cost)
# 	BookingDetail.objects.filter(order_id=order_id).update(status=update_status)


# def estimationCostCalculation(order_id, update_status):
# 	vehicle_price_per_km = BookingDetail.objects.filter(order_id=order_id).values('driver__vehicle__vehicletypes__per_km_price', 'order__location_detail')

# 	total_km = []
# 	price_per_km = []

	

# 	for i in vehicle_price_per_km:
# 		# print("i==>>", i)
# 		price_per_km.append(float(i['driver__vehicle__vehicletypes__per_km_price']))
# 		# print("i['order__location_detail']==>", i['order__location_detail'], 'type==>', type(i['order__location_detail']))
# 		if type(i['order__location_detail']) is not dict:
# 			for k in i['order__location_detail']:
# 				total_km.append(float(k['distance']['text'].replace('km', '')))                    
# 		else:
# 			total_km.append(float(i['order__location_detail']['distance']['text'].replace('km', '')))
			

# 	# print("total_km=>", total_km, sum(total_km))

# 	total_estimated_cost = price_per_km[0] * sum(total_km)

# 	# OrderDetails.objects.filter(id=order_id).update(total_estimated_cost=total_estimated_cost)
# 	# BookingDetail.objects.filter(order_id=order_id).update(status=update_status, total_amount=total_estimated_cost)
# 	BookingDetail.objects.filter(order_id=order_id).update(status=update_status)
# AIzaSyBOYh5wDV6N5l0FLqfwZI_HgtBJ9TiiPss
import requests
from django.conf import settings
from django.http import JsonResponse
# @method_decorator([authorization_required], name='dispatch')
class DriverAPI(APIView):
	def get(self, request):
		driver_id = request.query_params.get('driver_id')
		
		bookingDetail = BookingDetail.objects.filter(driver_id=driver_id).order_by('-id').values(
			'id', 'order_id', 'total_amount', 'order__user__first_name', 'order__user__last_name', 'order__user__mobile_number', 
			'status__status_name', 'order__location_detail', 'travel_details', 'order__total_estimated_cost', 'ordered_time',
			'pickedup_time', 'order_accepted_time', 'canceled_time', 'order_droped_time', 'driver_id', 'order__user__profile_image', 
			'assigned', 'order__checkorderotp__otp_json'
		)

		bookingDetailList = list(bookingDetail)

		for i in bookingDetailList:
			if i['total_amount'] is not None:
				i['total_amount'] = round(float(i['total_amount']), 1)

			if UserFeedback.objects.filter(Q(driver_id=driver_id) & Q(order_id=i['order_id']) & Q(rating_given_by="user")).exists():
				user_feedback_obj = UserFeedback.objects.filter(Q(driver_id=driver_id) & Q(order_id=i['order_id']) & Q(rating_given_by="user")).values()
				for j in list(user_feedback_obj):
					if i['driver_id'] == j['driver_id']:
						i['ratings'] = j['rating']
			elif i['status__status_name'] == 'Trip Ended':
				i['ratings'] = None

			# Ensure otp_json is properly initialized and set default values
			otp_json_data = i.get('order__checkorderotp__otp_json')
			if otp_json_data is None:
				otp_json_data = {}

			# Set default values for keys if not already set
			defaults = {
				'pick1': True,
				'pick2': False,
				'drop1': False,
				'drop2': False
			}
			
			for key, value in defaults.items():
				if key not in otp_json_data:
					otp_json_data[key] = value

			# Update the dictionary in the list
			i['otp_json'] = otp_json_data  # Assigning the updated otp_json to the dictionary

		return Response({'message': 'your orders are', 'data': bookingDetailList})
	def post(self, request):
		data = request.data
		order_id = data.get('order_id')
		update_status = data.get('update_status')
		driver_id = data.get('driver_id') 
		otp = data.get('otp') 
		otp_json = data.get('otp_json') 
		phone_number = data.get('phone_number') 
		is_last_number = data.get('is_last_number') 
		pickup_drop_details = data.get('pickup_drop_details') 
		order_detail = data.get('order_detail')
		if phone_number and otp:
			verified_otp = verifyOTP(phone_number, otp, datetime.now().timestamp(), order_id, otp_json, pickup_drop_details)
			if is_last_number:
				BookingDetail.objects.filter(order_id=order_id).update(is_all_mobile_number_verified=True, otp_json=otp_json)
				return Response({'status': '11', 'data': verified_otp})

			BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status)
			return Response({'status': '12', 'data': verified_otp})
		if update_status == str(8) and order_detail:
			statusRecord.objects.create(order_id=order_id, user_id=order_detail['user_id'], status_id=update_status, driver_id=order_detail['driver_id'])
			BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status, request_cancel=order_detail['request'])
			return Response({'message': 'requested for cancelation'})
		if update_status == str(9):
			statusRecord.objects.filter(order_id=order_id).update(is_accepted=order_detail['is_accepted'], user_id=order_detail['user_id'], driver_id=order_detail['driver_id'])
			BookingDetail.objects.filter(order_id=order_id).update(status=update_status, request_cancel=order_detail['request'])
			return Response({'message': 'cancelation request accepted successfully'})
		if update_status == str(10):
			statusRecord.objects.filter(order_id=order_id).update(is_accepted=order_detail['is_accepted'], user_id=order_detail['user_id'], driver_id=order_detail['driver_id'])
			BookingDetail.objects.filter(order_id=order_id).update(status=update_status, request_cancel=order_detail['request'])
			return Response({'message': 'cancelation request declined successfully'})
		if update_status == str(4):  # Trip Ended status id is 4
			estimationCostCalculation(order_id, update_status)
			BookingDetail.objects.filter(order_id=order_id).update(status=update_status, order_droped_time=datetime.now())
			booking_detail = BookingDetail.objects.get(order_id=order_id)
			order_accepted_time = booking_detail.order_accepted_time
			order_dropped_time = booking_detail.order_droped_time
			actual_time_taken_by_driver = order_dropped_time - order_accepted_time
			BookingDetail.objects.filter(order_id=order_id).update(actual_time_taken_to_complete=actual_time_taken_by_driver)
			return Response({'message': 'order updated successfully'})
		if update_status == str(5):
			estimationCostCalculation(order_id, update_status)
			BookingDetail.objects.filter(order_id=order_id).update(status=update_status, canceled_time=datetime.now())
			return Response({'message': 'order updated successfully'})
		if update_status == str(3):
			BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status, declined_time=datetime.now())
			return Response({'message': 'order updated successfully'})
		if update_status == str(2):
			if driver_id:
				BookingDetail.objects.filter(order_id=order_id).update(status=update_status, order_accepted_time=datetime.now(), driver_id=driver_id)
				estimationCostCalculation(order_id, update_status)
			otp = random.randint(100000, 999999)
			request.session['user_order_otp'] = otp
			OrderDetails.objects.filter(id=order_id).update(otp=otp)
			BookingDetail.objects.filter(order_id=order_id).update(status=update_status, order_accepted_time=datetime.now())
			location_details = OrderDetails.objects.get(id=order_id)
			return Response({'message': 'order updated successfully', 'location_details': location_details.location_detail})
		if otp:
			if OrderDetails.objects.get(id=order_id).otp == otp:
				BookingDetail.objects.filter(order_id=order_id).update(status=update_status, pickedup_time=datetime.now())
				return Response({'message': 'order updated successfully'})
			else:
				return Response({'message': 'otp doesnt match'}, status=status.HTTP_406_NOT_ACCEPTABLE)
			BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status, canceled_time=datetime.now())
		return Response({'message': 'order updated successfully'})
	# def post(self, request):
	# 	data = request.data

	# 	order_id = request.data.get('order_id')
	# 	update_status = data['update_status']
	# 	# driver_id = data['driver_id']
	# 	otp = request.data['otp']

	# 	otp_json = request.data.get('otp_json')
		
	# 	phone_number = request.data['phone_number']
	# 	is_last_number = request.data['is_last_number']

	# 	pickup_drop_details = request.data.get('pickup_drop_details')
               

	# 	if phone_number is not None and otp is not None:
	# 		verified_otp = verifyOTP(phone_number, otp, datetime.now().timestamp(), order_id, otp_json, pickup_drop_details)

	# 		if is_last_number == True:
	# 			res=BookingDetail.objects.filter(order_id=order_id).update(is_all_mobile_number_verified=True,otp_json=otp_json)
	# 			print('res----------',res)
	# 			return Response({'status': '11', 'data': verified_otp})

	# 		BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status)
		
	# 		return Response({'status': '12', 'data': verified_otp})
		
	# 	if((update_status == str(8)) & (data['order_detail'] is not None)):
	# 		statusRecord.objects.create(order_id=order_id, user_id = data['order_detail']['user_id'], status_id=update_status, driver_id=data['order_detail']['driver_id'])
	# 		BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status,request_cancel=data['order_detail']['request'])
	# 		return Response({'message': 'requested for cancelation'})
	# 	if(update_status == str(9)):
	# 		statusRecord.objects.filter(order_id=order_id).update(is_accepted=data['order_detail']['is_accepted'], user_id = data['order_detail']['user_id'], driver_id=data['order_detail']['driver_id'])
	# 		BookingDetail.objects.filter(order_id=order_id).update(status=update_status, request_cancel=data['order_detail']['request'])
	# 		return Response({'message': 'cancelation request accepted successfully'})
	# 	if(update_status == str(10)):
	# 		statusRecord.objects.filter(order_id=order_id).update(is_accepted=data['order_detail']['is_accepted'],user_id = data['order_detail']['user_id'], driver_id=data['order_detail']['driver_id'])
	# 		BookingDetail.objects.filter(order_id=order_id).update(status=update_status, request_cancel=data['order_detail']['request'])
	# 		return Response({'message': 'cancelation request declined successfully'})
	# 	if(update_status == str(4)): #Trip Ended status id is 4
	# 		estimationCostCalculation(order_id, update_status)

	# 		BookingDetail.objects.filter(order_id=order_id).update(status=update_status, order_droped_time=datetime.now())

	# 		order_accepted_time = BookingDetail.objects.get(order_id=order_id).order_accepted_time
	# 		order_dopped_time = BookingDetail.objects.get(order_id=order_id).order_droped_time

	# 		order_accepted_start_time = str(order_accepted_time).split()[1]
	# 		order_dopped_time_end_time = str(order_dopped_time).split()[1]

	# 		start_time = str(order_accepted_start_time).split("+")[0].split(':')
	# 		end_time = str(order_dopped_time_end_time).split("+")[0].split(':')

	# 		t1 = datetime.strptime(start_time[0]+":"+start_time[1]+":"+str(00), "%H:%M:%S")
	# 		# print('Start time:', t1.time())

	# 		t2 = datetime.strptime(end_time[0]+":"+end_time[1]+":"+str(00), "%H:%M:%S")
	# 		# print('End time:', t2.time())

	# 		actual_time_taken_by_driver = t2 - t1

	# 		BookingDetail.objects.filter(order_id=order_id).update(actual_time_taken_to_complete=actual_time_taken_by_driver)

	# 		return Response({'message': 'order updated successfully'})
	# 	if (update_status == str(5)):
	# 		estimationCostCalculation(order_id, update_status)
	# 		BookingDetail.objects.filter(order_id=order_id).update(status=update_status, canceled_time=datetime.now())
	# 		return Response({'message': 'order updated successfully'})
	# 	if(update_status == str(3)):
	# 		BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status, declined_time=datetime.now())
	# 		return Response({'message': 'order updated successfully'})
	# 	if(update_status == str(2)):
	# 		if data['driver_id'] is not None:
	# 			BookingDetail.objects.filter(order_id=order_id).update(status=update_status, order_accepted_time=datetime.now(), driver_id=data['driver_id'])
	# 			estimationCostCalculation(order_id, update_status)

	# 		# driver_obj = Driver.objects.get(user_id=data['driver_id'])
	# 		# vehicle_obj = Vehicle.objects.get(id=vehicle_id)

	# 		estimationCostCalculation(order_id, update_status)
	# 		otp = random.randint(100000, 999999)
			
	# 		request.session['user_order_otp'] = otp
	# 		OrderDetails.objects.filter(id=order_id).update(otp=otp)
			
	# 		BookingDetail.objects.filter(order_id=order_id).update(status=update_status, order_accepted_time=datetime.now())
	# 		location_details = OrderDetails.objects.get(id=order_id)
	# 		return Response({'message': 'order updated successfully', 'location_details': location_details.location_detail})
	# 	if data['otp'] is not None:
	# 		if OrderDetails.objects.get(id=order_id).otp == data['otp']:
	# 			BookingDetail.objects.filter(order_id=order_id).update(status=update_status, pickedup_time=datetime.now())
	# 			return Response({'message': 'order updated successfully'})
	# 		else:
	# 			return Response({'message': 'otp doesnt match'}, status=status.HTTP_406_NOT_ACCEPTABLE)
	# 	else:
	# 		BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status, canceled_time=datetime.now())
	# 		return Response({'message': 'order updated successfully'})

	
# class DriverAPI(APIView):
#     def calculate_distance_eta(self, origin_lat, origin_lng, dest_lat, dest_lng):
#         try:
#             response = requests.get(
#                 f"https://maps.googleapis.com/maps/api/distancematrix/json",
#                 params={
#                     "origins": f"{origin_lat},{origin_lng}",
#                     "destinations": f"{dest_lat},{dest_lng}",
#                     "key": "AIzaSyBOYh5wDV6N5l0FLqfwZI_HgtBJ9TiiPss"  # Replace with your actual API key
#                 }
#             )
#             response.raise_for_status()  # Raise an exception for HTTP errors
#             distance_data = response.json()

#             if "rows" in distance_data and distance_data["rows"]:
#                 elements = distance_data["rows"][0]["elements"]
#                 if elements and "duration" in elements[0]:
#                     eta_seconds = elements[0]["duration"]["value"]
#                     print('ETA Seconds:', eta_seconds)
#                     return eta_seconds
#             else:
#                 print('Distance Matrix API response:', distance_data)
#                 return None  # Return None if ETA not available
#         except requests.exceptions.RequestException as e:
#             print("Error fetching ETA:", e)
#         except Exception as e:
#             print("Error:", e)

#         return None

#     def get(self, request):    
#         bookingDetail = BookingDetail.objects.filter(driver_id=request.query_params['driver_id']).order_by('-id').values(
#                 'id','order_id', 'total_amount', 'order__user__first_name', 'order__user__last_name', 'order__user__mobile_number', 'status__status_name', 'order__location_detail', 'travel_details', 'order__total_estimated_cost',
#                 'ordered_time','pickedup_time','order_accepted_time','canceled_time','order_droped_time', 'driver_id', 'order__user__profile_image', 'assigned')

#         for i in list(bookingDetail):
#             if i['total_amount'] is not None:
#                 i['total_amount'] = round(float(i['total_amount']), 1)

#             # Extract start_location and end_location from order_location_detail
#             if 'order__location_detail' in i:
#                 location_detail = i['order__location_detail']
#                 if location_detail and 'steps' in location_detail:
#                     steps = location_detail['steps']
#                     if steps:
#                         first_step = steps[0]
#                         last_step = steps[-1]
#                         i['start_location'] = first_step.get('start_location', None)
#                         i['end_location'] = last_step.get('end_location', None)

#                         # Calculate ETA between start_location and end_location
#                         eta_seconds = self.calculate_distance_eta(
#                             i['start_location']['lat'],
#                             i['start_location']['lng'],
#                             i['end_location']['lat'],
#                             i['end_location']['lng']
#                         )
#                         i['eta_seconds'] = eta_seconds

#                         # Convert ETA from seconds to minutes
#                         i['eta_minutes'] = eta_seconds / 60

#                         # Print start_location, end_location, and ETA in minutes
#                         print('Start Location:', i['start_location'])
#                         print('End Location:', i['end_location'])
#                         print('ETA Seconds:', eta_seconds)
#                         print('ETA Minutes:', i['eta_minutes'])

#                         # Store eta_minutes in a variable for response
#                         eta_minutes_value = i['eta_minutes']

#             # Check if there's user feedback and update ratings accordingly
#             if UserFeedback.objects.filter(Q(driver_id=request.query_params['driver_id']) & Q(order_id=i['order_id']) & Q(rating_given_by="user")).exists():
#                 user_feedback_obj = UserFeedback.objects.filter(Q(driver_id=request.query_params['driver_id']) & Q(order_id=i['order_id']) & Q(rating_given_by="user")).values()
#                 for j in list(user_feedback_obj):
#                     if i['driver_id'] == j['driver_id']:
#                         i['ratings'] = j['rating']

#             elif i['status__status_name'] == 'Trip Ended':
#                 i['ratings'] = None

#         # Construct the response with the updated data including ETA in minutes
#         response_data = {'eta_minutes': eta_minutes_value, 'message': 'your orders are', 'data': bookingDetail}
#         print('Response Data:', response_data)
#         return Response(response_data)
            
#     def post(self, request):
#         data = request.data

#         order_id = data['order_id']
#         update_status = data['update_status']
#         # driver_id = data['driver_id']
#         otp = request.data['otp']

#         otp_json = request.data.get('otp_json')
        
#         phone_number = request.data['phone_number']
#         is_last_number = request.data['is_last_number']

#         pickup_drop_details = request.data.get('pickup_drop_details')
               

#         if phone_number is not None and otp is not None:
#             verified_otp = verifyOTP(phone_number, otp, datetime.now().timestamp(), order_id, otp_json, pickup_drop_details)

#             if is_last_number == True:
#                 BookingDetail.objects.filter(order_id=order_id).update(is_all_mobile_number_verified=True)
#                 return Response({'status': '11', 'data': verified_otp})

#             BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status)
        
#             return Response({'status': '12', 'data': verified_otp})
        
#         if((update_status == str(8)) & (data['order_detail'] is not None)):
#             statusRecord.objects.create(order_id=order_id, user_id = data['order_detail']['user_id'], status_id=update_status, driver_id=data['order_detail']['driver_id'])
#             BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status,request_cancel=data['order_detail']['request'])
#             return Response({'message': 'requested for cancelation'})
#         if(update_status == str(9)):
#             statusRecord.objects.filter(order_id=order_id).update(is_accepted=data['order_detail']['is_accepted'], user_id = data['order_detail']['user_id'], driver_id=data['order_detail']['driver_id'])
#             BookingDetail.objects.filter(order_id=order_id).update(status=update_status, request_cancel=data['order_detail']['request'])
#             return Response({'message': 'cancelation request accepted successfully'})
#         if(update_status == str(10)):
#             statusRecord.objects.filter(order_id=order_id).update(is_accepted=data['order_detail']['is_accepted'],user_id = data['order_detail']['user_id'], driver_id=data['order_detail']['driver_id'])
#             BookingDetail.objects.filter(order_id=order_id).update(status=update_status, request_cancel=data['order_detail']['request'])
#             return Response({'message': 'cancelation request declined successfully'})
#         if(update_status == str(4)): #Trip Ended status id is 4
#             estimationCostCalculation(order_id, update_status)

#             BookingDetail.objects.filter(order_id=order_id).update(status=update_status, order_droped_time=datetime.now())

#             order_accepted_time = BookingDetail.objects.get(order_id=order_id).order_accepted_time
#             order_dopped_time = BookingDetail.objects.get(order_id=order_id).order_droped_time

#             order_accepted_start_time = str(order_accepted_time).split()[1]
#             order_dopped_time_end_time = str(order_dopped_time).split()[1]

#             start_time = str(order_accepted_start_time).split("+")[0].split(':')
#             end_time = str(order_dopped_time_end_time).split("+")[0].split(':')

#             t1 = datetime.strptime(start_time[0]+":"+start_time[1]+":"+str(00), "%H:%M:%S")
#             # print('Start time:', t1.time())

#             t2 = datetime.strptime(end_time[0]+":"+end_time[1]+":"+str(00), "%H:%M:%S")
#             # print('End time:', t2.time())

#             actual_time_taken_by_driver = t2 - t1

#             BookingDetail.objects.filter(order_id=order_id).update(actual_time_taken_to_complete=actual_time_taken_by_driver)

#             return Response({'message': 'order updated successfully'})
#         if (update_status == str(5)):
#             estimationCostCalculation(order_id, update_status)
#             BookingDetail.objects.filter(order_id=order_id).update(status=update_status, canceled_time=datetime.now())
#             return Response({'message': 'order updated successfully'})
#         if(update_status == str(3)):
#             BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status, declined_time=datetime.now())
#             return Response({'message': 'order updated successfully'})
#         if(update_status == str(2)):
#             if data['driver_id'] is not None:
#                 BookingDetail.objects.filter(order_id=order_id).update(status=update_status, order_accepted_time=datetime.now(), driver_id=data['driver_id'])
#                 estimationCostCalculation(order_id, update_status)

#             # driver_obj = Driver.objects.get(user_id=data['driver_id'])
#             # vehicle_obj = Vehicle.objects.get(id=vehicle_id)

#             estimationCostCalculation(order_id, update_status)
#             otp = random.randint(100000, 999999)
            
#             request.session['user_order_otp'] = otp
#             OrderDetails.objects.filter(id=order_id).update(otp=otp)
            
#             BookingDetail.objects.filter(order_id=order_id).update(status=update_status, order_accepted_time=datetime.now())
#             location_details = OrderDetails.objects.get(id=order_id)
#             return Response({'message': 'order updated successfully', 'location_details': location_details.location_detail})
#         if data['otp'] is not None:
#             if OrderDetails.objects.get(id=order_id).otp == data['otp']:
#                 BookingDetail.objects.filter(order_id=order_id).update(status=update_status, pickedup_time=datetime.now())
#                 return Response({'message': 'order updated successfully'})
#             else:
#                 return Response({'message': 'otp doesnt match'}, status=status.HTTP_406_NOT_ACCEPTABLE)
#         else:
#             BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status, canceled_time=datetime.now())
#             return Response({'message': 'order updated successfully'})
# class DriverAPI(APIView):
    # def calculate_distance_eta(self, origin_lat, origin_lng, dest_lat, dest_lng):
    #     try:
    #         response = requests.get(
    #             f"https://maps.googleapis.com/maps/api/distancematrix/json",
    #             params={
    #                 "origins": f"{origin_lat},{origin_lng}",
    #                 "destinations": f"{dest_lat},{dest_lng}",
    #                 "key": "AIzaSyBOYh5wDV6N5l0FLqfwZI_HgtBJ9TiiPss"  # Replace with your actual API key
    #             }
    #         )
    #         response.raise_for_status()  # Raise an exception for HTTP errors
    #         distance_data = response.json()

    #         if "rows" in distance_data and distance_data["rows"]:
    #             elements = distance_data["rows"][0]["elements"]
    #             if elements and "duration" in elements[0]:
    #                 eta_seconds = elements[0]["duration"]["value"]
    #                 print('ETA Seconds:', eta_seconds)
    #                 return eta_seconds
    #         else:
    #             print('Distance Matrix API response:', distance_data)
    #             return None  # Return None if ETA not available
    #     except requests.exceptions.RequestException as e:
    #         print("Error fetching ETA:", e)
    #     except Exception as e:
    #         print("Error:", e)

    #     return None

#     def get(self, request):    
#         bookingDetail = BookingDetail.objects.filter(driver_id=request.query_params['driver_id']).order_by('-id').values(
#                 'id','order_id', 'total_amount', 'order__user__first_name', 'order__user__last_name', 'order__user__mobile_number', 'status__status_name', 'order__location_detail', 'travel_details', 'order__total_estimated_cost',
#                 'ordered_time','pickedup_time','order_accepted_time','canceled_time','order_droped_time', 'driver_id', 'order__user__profile_image', 'assigned')

#         for i in list(bookingDetail):
#             if i['total_amount'] is not None:
#                 i['total_amount'] = round(float(i['total_amount']), 1)

#             # Extract start_location and end_location from order_location_detail
#             if 'order__location_detail' in i:
#                 location_detail = i['order__location_detail']
#                 if location_detail and 'steps' in location_detail:
#                     steps = location_detail['steps']
#                     if steps:
#                         first_step = steps[0]
#                         last_step = steps[-1]
#                         i['start_location'] = first_step.get('start_location', None)
#                         i['end_location'] = last_step.get('end_location', None)

#                         # Calculate ETA between start_location and end_location
#                         eta_seconds = self.calculate_distance_eta(
#                             i['start_location']['lat'],
#                             i['start_location']['lng'],
#                             i['end_location']['lat'],
#                             i['end_location']['lng']
#                         )
#                         i['eta_seconds'] = eta_seconds

#                         # Convert ETA from seconds to minutes
#                         i['eta_minutes'] = eta_seconds / 60
#                         eta_min=i['eta_minutes'] # Correct indentation here
#                         # Print start_location, end_location, and ETA in minutes
#                         print('Start Location:', i['start_location'])
#                         print('End Location:', i['end_location'])
#                         print('ETA Seconds:', eta_seconds)
#                         print('ETA Minutes:', i['eta_minutes'])

#             # Check if there's user feedback and update ratings accordingly
#             if UserFeedback.objects.filter(Q(driver_id=request.query_params['driver_id']) & Q(order_id=i['order_id']) & Q(rating_given_by="user")).exists():
#                 user_feedback_obj = UserFeedback.objects.filter(Q(driver_id=request.query_params['driver_id']) & Q(order_id=i['order_id']) & Q(rating_given_by="user")).values()
#                 for j in list(user_feedback_obj):
#                     if i['driver_id'] == j['driver_id']:
#                         i['ratings'] = j['rating']

#             elif i['status__status_name'] == 'Trip Ended':
#                 i['ratings'] = None

#         # Construct the response with the updated data including ETA in minutes
#         response_data = {'eta_min':eta_min,'message': 'your orders are', 'data': bookingDetail}
#         print('Response Data:', response_data)
#         return Response(response_data)

#     def post(self, request):
#         data = request.data

#         order_id = data['order_id']
#         update_status = data['update_status']
#         otp = request.data['otp']
#         otp_json = request.data.get('otp_json')
#         phone_number = request.data['phone_number']
#         is_last_number = request.data['is_last_number']
#         pickup_drop_details = request.data.get('pickup_drop_details')
               

#         if phone_number is not None and otp is not None:
#             verified_otp = verifyOTP(phone_number, otp, datetime.now().timestamp(), order_id, otp_json, pickup_drop_details)

#             if is_last_number == True:
#                 BookingDetail.objects.filter(order_id=order_id).update(is_all_mobile_number_verified=True)
#                 return Response({'status': '11', 'data': verified_otp})

#             BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status)
        
#             return Response({'status': '12', 'data': verified_otp})
        
#         if((update_status == str(8)) & (data['order_detail'] is not None)):
#             statusRecord.objects.create(order_id=order_id, user_id = data['order_detail']['user_id'], status_id=update_status, driver_id=data['order_detail']['driver_id'])
#             BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status,request_cancel=data['order_detail']['request'])
#             return Response({'message': 'requested for cancelation'})
#         if(update_status == str(9)):
#             statusRecord.objects.filter(order_id=order_id).update(is_accepted=data['order_detail']['is_accepted'], user_id = data['order_detail']['user_id'], driver_id=data['order_detail']['driver_id'])
#             BookingDetail.objects.filter(order_id=order_id).update(status=update_status, request_cancel=data['order_detail']['request'])
#             return Response({'message': 'cancelation request accepted successfully'})
#         if(update_status == str(10)):
#             statusRecord.objects.filter(order_id=order_id).update(is_accepted=data['order_detail']['is_accepted'],user_id = data['order_detail']['user_id'], driver_id=data['order_detail']['driver_id'])
#             BookingDetail.objects.filter(order_id=order_id).update(status=update_status, request_cancel=data['order_detail']['request'])
#             return Response({'message': 'cancelation request declined successfully'})
#         if(update_status == str(4)): #Trip Ended status id is 4
#             estimationCostCalculation(order_id, update_status)

#             BookingDetail.objects.filter(order_id=order_id).update(status=update_status, order_droped_time=datetime.now())

#             order_accepted_time = BookingDetail.objects.get(order_id=order_id).order_accepted_time
#             order_dopped_time = BookingDetail.objects.get(order_id=order_id).order_droped_time

#             order_accepted_start_time = str(order_accepted_time).split()[1]
#             order_dopped_time_end_time = str(order_dopped_time).split()[1]

#             start_time = str(order_accepted_start_time).split("+")[0].split(':')
#             end_time = str(order_dopped_time_end_time).split("+")[0].split(':')

#             t1 = datetime.strptime(start_time[0]+":"+start_time[1]+":"+str(00), "%H:%M:%S")
#             t2 = datetime.strptime(end_time[0]+":"+end_time[1]+":"+str(00), "%H:%M:%S")

#             actual_time_taken_by_driver = t2 - t1

#             BookingDetail.objects.filter(order_id=order_id).update(actual_time_taken_to_complete=actual_time_taken_by_driver)

#             return Response({'message': 'order updated successfully'})
#         if (update_status == str(5)):
#             estimationCostCalculation(order_id, update_status)
#             BookingDetail.objects.filter(order_id=order_id).update(status=update_status, canceled_time=datetime.now())
#             return Response({'message': 'order updated successfully'})
#         if(update_status == str(3)):
#             BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status, declined_time=datetime.now())
#             return Response({'message': 'order updated successfully'})
#         if(update_status == str(2)):
#             if data['driver_id'] is not None:
#                 BookingDetail.objects.filter(order_id=order_id).update(status=update_status, order_accepted_time=datetime.now(), driver_id=data['driver_id'])
#                 estimationCostCalculation(order_id, update_status)

#             estimationCostCalculation(order_id, update_status)
#             otp = random.randint(100000, 999999)
            
#             request.session['user_order_otp'] = otp
#             OrderDetails.objects.filter(id=order_id).update(otp=otp)
            
#             BookingDetail.objects.filter(order_id=order_id).update(status=update_status, order_accepted_time=datetime.now())
#             location_details = OrderDetails.objects.get(id=order_id)
#             return Response({'message': 'order updated successfully', 'location_details': location_details.location_detail})
#         if data['otp'] is not None:
#             if OrderDetails.objects.get(id=order_id).otp == data['otp']:
#                 BookingDetail.objects.filter(order_id=order_id).update(status=update_status, pickedup_time=datetime.now())
#                 return Response({'message': 'order updated successfully'})
#             else:
#                 return Response({'message': 'otp doesnt match'}, status=status.HTTP_406_NOT_ACCEPTABLE)
#         else:
#             BookingDetail.objects.filter(order_id=order_id).update(status_id=update_status, canceled_time=datetime.now())
#             return Response({'message': 'order updated successfully'})
@method_decorator([authorization_required], name='dispatch')
class UpdateDriveOnlineApi(APIView):
	# from datetime import datetime
	def post(self, request):
		data = request.data

		driver_id = data['driver_id']
		is_online = data['is_online']
		
		if is_online:
			Driver.objects.filter(user_id=driver_id).update(is_online=is_online, date_online=datetime.now())
		else:
			Driver.objects.filter(user_id=driver_id).update(is_online=is_online, date_offline=datetime.now())
		return Response({'message': 'user online status updated successfully'})

@method_decorator([authorization_required], name='dispatch')
class DriverOrderAPI(APIView):
	def get(self, request):
		data = request.data
		rating = data.get('rating')
		driver_id = request.query_params.get('driver_id')
		order_id = request.query_params.get('order_id')
		
		bookingDetail = BookingDetail.objects.filter(driver_id=driver_id, order_id=order_id).values(
			'order_id', 'total_amount', 'order__user__first_name', 'order__checkorderotp__otp_json', 'order__user_id',
			'order__user__last_name', 'order__user__mobile_number', 'status__status_name',
			'travel_details', 'order__total_estimated_cost', 'request_cancel', 'order__user__profile_image_path', 
			'sub_user_phone_numbers'
		)
		
		bookingDetailList = list(bookingDetail)
		
		for i in bookingDetailList:
			user_id = i['order__user_id']

			# Ensure otp_json is properly initialized and set default values
			otp_json_data = i.get('order__checkorderotp__otp_json')
			if otp_json_data is None:
				otp_json_data = {}

			# Set default values for keys if not already set
			defaults = {
				'pick1': True,
				'pick2': False,
				'drop1': False,
				'drop2': False
			}
			
			for key, value in defaults.items():
				if key not in otp_json_data:
					otp_json_data[key] = value

			# Update the dictionary in the list
			i['otp_json'] = otp_json_data

		user_rating = UserFeedback.objects.filter(rating_given_by="driver", user_id=user_id).values('rating')
		average_rating = user_rating.aggregate(Avg('rating'))
		
		if average_rating['rating__avg'] is None:
			rating = 5
		else:
			rating = round(average_rating['rating__avg'], 1)

		return Response({'message': 'your orders are', 'data': bookingDetailList, 'rating': rating})
	# def get(self, request):
	# 	data=request.data
	# 	rating=data.get('rating')
	# 	driver_id = request.query_params.get('driver_id')
	# 	bookingDetail = BookingDetail.objects.filter(driver_id=request.query_params['driver_id'],order_id=request.query_params['order_id']).values(
	# 			'order_id', 'total_amount', 'order__user__first_name','order__user_id', 'order__user__last_name', 'order__user__mobile_number', 'status__status_name', 'otp_json','order__location_detail', 'travel_details', 'order__total_estimated_cost', 'request_cancel', 'order__user__profile_image_path','sub_user_phone_numbers'
	# 		)
	# 	print('bookingDetail-----------------------------',)
	# 	for i in bookingDetail:
	# 		user_id = i['order__user_id']

	# 	print(user_id)


	# 	user_rating=UserFeedback.objects.filter(rating_given_by="driver", user_id=user_id).values('rating')
	# 	print("user_rating==>", user_rating)
	# 	average_rating=user_rating.aggregate(Avg('rating'))
	# 	print("average_rating==>", average_rating)
	# 	if average_rating['rating__avg'] is None:
	# 		rating =5
	# 		return Response({'message': 'your orders are', 'data': bookingDetail,'rating':rating})
		
	# 	return Response({'message': 'your orders are', 'data': bookingDetail,'rating': round(average_rating['rating__avg'], 1)})


@method_decorator([authorization_required], name='dispatch')
class updateDriverLocation(APIView):
	def get(self, request):
		driver_obj = Driver.objects.filter(user_id=request.query_params['driver_id']).values(
				'live_lattitude',
				'live_longitude'
			)
		return Response({'data': driver_obj})

	def put(self, request):
		if Driver.objects.filter(user_id=request.data['driver_id']).exists():
			Driver.objects.filter(user_id=request.data['driver_id']).update(
				live_lattitude = request.data['lat'],
				live_longitude = request.data['lng']
			)

			if BookingDetail.objects.filter(driver_id=request.data['driver_id']).exists():
				latest_booking_id = BookingDetail.objects.filter(driver_id=request.data['driver_id']).values('order__location_detail').latest('id')
				# print('latest_booking_id==>>', latest_booking_id['order__location_detail'])

				if isinstance(latest_booking_id['order__location_detail'], dict):
					start_location = latest_booking_id['order__location_detail']['start_location']

					user_lat = start_location['lat']
					user_lng = start_location['lng']

					coords_1 = (request.data['lat'], request.data['lng'])
					coords_2 = (user_lat, user_lng)

					# print("total km",geopy.distance.geodesic(coords_1, coords_2).km)

					if geopy.distance.geodesic(coords_1, coords_2).km < 2:
						return Response({'message': 'you are nearer to user'})
				else:
					print()
					# print("not a dictionary")

			return Response({'message': 'location updated successfully'})
		return Response({'err': 'driver not found'}) 

	# def put(self, request):
	# 	if Driver.objects.filter(user_id=request.data['driver_id']).exists():
	# 		Driver.objects.filter(user_id=request.data['driver_id']).update(
	# 			live_lattitude = request.data['lat'],
	# 			live_longitude = request.data['lng']
	# 		)

	# 		if BookingDetail.objects.filter(driver_id=request.data['driver_id']).exists():
	# 			latest_booking_id = BookingDetail.objects.filter(driver_id=request.data['driver_id']).values('order__location_detail').latest('id')
	# 			print('latest_booking_id==>>', latest_booking_id['order__location_detail'])

	# 			if latest_booking_id['order__location_detail'] != dict:
	# 				latest_booking_id['order__location_detail']['start_location'] 

	# 				user_lat = latest_booking_id['order__location_detail']['start_location']['lat']
	# 				user_lng = latest_booking_id['order__location_detail']['start_location']['lng']

	# 				coords_1 = (request.data['lat'], request.data['lng'])
	# 				coords_2 = (user_lat, user_lng)

	# 				print("total km",geopy.distance.geodesic(coords_1, coords_2).km)

	# 				if geopy.distance.geodesic(coords_1, coords_2).km < 2:
	# 					return Response({'message': 'you are nearer to user'})
	# 			else:
	# 				print("list")

	# 		return Response({'message': 'location updated successfully'})
	# 	return Response({'err': 'driver not found'})

from django.db.models import Avg
# qs.filter(amount=Floor('amount'))

@method_decorator([authorization_required], name='dispatch')
class DriverEarningsAndratingAPI(APIView):
	def get(self, request):
		data=request.data
		driver_id = request.query_params.get('driver_id')
		# print("driver_id",driver_id)
		user_id = request.query_params.get('user_id')
		# print("user_id",user_id)
		id = request.query_params.get('id')
		# print("id",id)

		if id:
			id_obj=UserFeedback.objects.filter(id=id).values()
			# print("id_obj",id_obj)
			return Response({'data':id_obj})
		if driver_id:
			driver_obj=UserFeedback.objects.filter(Q(driver_id=driver_id) & Q(rating_given_by="user")).values('rating')
			# print("driver_obj",driver_obj)
			average_rating=driver_obj.aggregate(Avg('rating'))
			print("average_rating",average_rating)
			if average_rating['rating__avg'] is None:
				return Response({'average_rating': 5.0})
			return Response({'average_rating': round(average_rating['rating__avg'], 1)})
		if user_id:
			user_obj=UserFeedback.objects.filter(Q(user_id=user_id) & Q(rating_given_by="driver")).values('rating')
			print("user_obj",user_obj)
			average_rating=user_obj.aggregate(Avg('rating'))
			# print("==>>",average_rating)
			if average_rating['rating__avg'] is None:
				return Response({'average_rating': 5.0})
			return Response({'average_rating': round(average_rating['rating__avg'], 1)})
		else:
			obj=UserFeedback.objects.all().values()
			return Response({'data':obj})
		# else:
		# 	obj = UserFeedback.objects.all().values()
        #     return Response({'data':obj})
		# rating_list = []

		# for i in booking_obj:
		# 	user_feedback_obj = UserFeedback.objects.filter(order_id=i['order_id']).values('rating')

		# 	for j in user_feedback_obj:
		# 		rating_list.append(int(j['rating']))

		# average_rating = sum(rating_list) / len(rating_list)

		# return Response({'message': 'rating details of driver', 'average_rating': average_rating})
		# if id:
		# 	userFeedback = UserFeedback.objects.filter(id = id).values('user','driver','rating','review','order','rating_given_by')
		# 	return Response({'data':userFeedback})
		


# remaining_days = datetime.datetime.strptime("2022-12-14", "%Y-%m-%d").date() - datetime.datetime.now().date()
# print(remaining_days)

@method_decorator([authorization_required], name='dispatch')
class NotifyDriverDocumentExpiry(APIView):
	def get(self, request):
		driver_id = request.query_params['driver_id']
		print(driver_id,"ddddddddddddddddd")
		driver_o = Driver.objects.filter(user_id=driver_id)
		print(driver_o,"gggg")

		driver_obj = Driver.objects.filter(user_id=driver_id).values('license_expire_date', 'insurance_expire_date','fitness_certificate_expire_date', 'vehicle__permit_expire_date', 'vehicle__rc_expire_date', 'vehicle__emission_certificate_expire_date')
		print(driver_obj,"ooooobbbb")

		# temp = min(dict(driver_obj[0]).values())
		# res = [key for key in dict(driver_obj[0]) if dict(driver_obj[0])[key] == temp]

		# print("res==>>", res)

		dateList = []
		dateDict = {}
		for k, v in dict(driver_obj[0]).items():
			# print("values===>>>",v, type(v))

			remaining_days = v - datetime.now().date()

			# print("remaining_days==>", remaining_days)

			days = str(remaining_days).replace("0:00:00", "").replace(",", "").replace("days", "").replace("day", "")
			
			
			document_name = k.replace("_expire_date", "").replace("__", " ").replace("_", " ")

			if days == "":
				days = 0
			print('days==>', days == "", days)
			if int(days) == 0:
				dateDict['document'] = k
				dateDict['days_remaining'] = " 0 days"
				dateDict['message'] = document_name.capitalize() +" is expiring today "
				dateDict['is_expired'] = 1
			elif int(days) < 30 and int(days) >= 0:
				dateDict['document'] = k
				dateDict['days_remaining'] = str(remaining_days).replace("0:00:00", "").replace(",", "")
				dateDict['message'] = document_name.capitalize() +" is expiring in "+str(remaining_days).replace("0:00:00", "").replace(",", "")
				dateDict['is_expired'] = 1
			elif int(days) < 0 :
				dateDict['document'] = k
				dateDict['expired'] = str(remaining_days).replace("0:00:00", "").replace(",", "").replace("-", "") + "ago"
				dateDict['message'] = document_name.capitalize()+" has expired "+ str(remaining_days).replace("0:00:00", "").replace(",", "").replace("-", "") + "ago ."
				dateDict['is_expired'] = 0
			if dateDict == {}:
				pass
			else:
				dateList.append(dateDict)
				dateDict = {}

		# print("min date",min(dateList))


		return Response({'data':dateList}) 


# @method_decorator([authorization_required], name='dispatch')
class DriverEarningReport(APIView):
	def get(self,request):
		year = request.query_params.get('year')
		month = request.query_params.get('month')
		week = request.query_params.get('week')
		driver_id = request.query_params.get('driver_id')

		dayList = []
		dayDict = {}
		yeardict ={
				"January":0,
				"February":0,
				"March":0,
				"April":0,
				"May":0,
				"June":0,
				"July":0,
				"August":0,
				"September":0,
				"October":0,
				"November":0,
				"December":0,
				
			}
			
		
		driver_obj = Driver.objects.get(user_id=driver_id)

		vehicle_id = driver_obj.vehicle_id

		Vehicle_number = Vehicle.objects.get(id=vehicle_id).vehicle_number

		print("Vehicle_number=>>", Vehicle_number)
		
		if Vehicle_number is None:
			return Response({'message': 'you have not started any earnigs', 'data': {}, 'is_data': 0})
		

		# query = BookingDetail.objects.select_related('order').filter(order__vehicle_number=Vehicle_number).values('order__total_estimated_cost', 'order_accepted_time')
		query = BookingDetail.objects.filter(Q(driver_id=driver_id) & Q(status_id=4)).values('order__total_estimated_cost', 'order_accepted_time', 'total_amount')


		# query = BookingDetail.objects.filter(driver_id=driver_id).values('order__total_estimated_cost', 'order_accepted_time')
		if driver_id and year is not None:
			# year_query = BookingDetail.objects.select_related('order').filter(order__vehicle_number=Vehicle_number, order_accepted_time__year=year).values('order__total_estimated_cost', 'order_accepted_time')
			year_query = BookingDetail.objects.filter(Q(driver_id=driver_id) & Q(status_id=4)).values('order__total_estimated_cost', 'order_accepted_time', 'total_amount')
			for i in year_query:
				print("year=========,",i)
				if i['order_accepted_time'] == None:
					pass
				else:					
					#dayDict['date'] = i['order_accepted_time'].year
					# dayDict['amount_earned'] = i['order__total_estimated_cost'] #dev server
					dayDict['amount_earned'] = float(i['total_amount']) # testing server
					dayDict['month']=i['order_accepted_time'].month
					dayDict['month_name']=i['order_accepted_time'].strftime("%B")
					# dayDict['vehicle_number'] = i['order__vehicle_number']
					dayList.append(dayDict)
					dayDict = {} 
					tempDate = []
					for i in range(0, len(dayList)):
						#print(m[i]['date'])
						tempDate.append(dayList[i]['month_name'])
	
					tempAmt = []
					# print(set(tempDate))
					for j in set(tempDate):
						# print(j)
						for k in dayList:
							# print(k)
							if j == k['month_name']:
								# print(k['amount_earned'])
								# print(j, k['date'], k['amount_earned'])
								tempAmt.append((k['month_name'], k['amount_earned']))

					result = {}
					for k, v in tempAmt:
						result.setdefault(k, []).append(v)

					finaloutput = []
					finalDict = {}
					# print(result)
					for z, y in result.items():
						yeardict[z]=sum(y)
			return Response ({'message': 'your earnings are','data':yeardict, 'is_data': 1})
			
		else:
			for i in query:
				# print(i)
				if i['order_accepted_time'] == None:
					pass
				else:					
					dayDict['date'] = i['order_accepted_time'].date()
					# dayDict['amount_earned'] = i['order__total_estimated_cost'] #dev server
					dayDict['amount_earned'] = float(i['total_amount']) # testing server
					dayDict['month']=i['order_accepted_time'].month
					# dayDict['vehicle_number'] = i['order__vehicle_number']
					dayList.append(dayDict)
					dayDict = {} 
					tempDate = []
					for i in range(0, len(dayList)):
						#print(m[i]['date'])
						tempDate.append(dayList[i]['date'])
	
					tempAmt = []
					# print(set(tempDate))
					for j in set(tempDate):
						# print(j)
						for k in dayList:
							# print(k)
							if j == k['date']:
								# print(k['amount_earned'])
								# print(j, k['date'], k['amount_earned'])
								tempAmt.append((k['date'], k['amount_earned']))

					# print(tempAmt)

					result = {}
					for k, v in tempAmt:
						result.setdefault(k, []).append(v)

					finaloutput = []
					finalDict = {}
					# print(result)
					for z, y in result.items():
						# print(z, sum(y))
						finalDict['date'] = z
						finalDict['amount'] = sum(y)
						finaloutput.append(finalDict)
						finalDict = {}

					# print(finaloutput)
			

		# print("pringting query==>",query.query)
			return Response ({'message': 'your earnings are','data':finaloutput, 'is_data': 1})


@method_decorator([authorization_required], name='dispatch')
class AssignVehicleToDriver(APIView):
	def post(self, request):
		vehicle_id = request.data['vehicle_id']
		# old_driver_id = request.data['old_driver_id']
		new_driver_id = request.data['driver_id']

		# print(vehicle_id, new_driver_id)

		old_driver_id = Driver.objects.get(vehicle_id=vehicle_id).user_id

		new_driver_vehicle_id = Driver.objects.get(user_id=new_driver_id).vehicle_id

		# print("new_driver_id==>", new_driver_id, "vehicle_id=>", vehicle_id, "old_driver_id=>", old_driver_id, "new_driver_vehicle_id==>",new_driver_vehicle_id)

		if VehicleAssingedToDriver.objects.filter(Q(vehicle_id_id=vehicle_id) & Q(old_driver_id=old_driver_id) & Q(new_driver_id=new_driver_id)).exists():
			print("HI")
			
			VehicleAssingedToDriver.objects.filter(vehicle_id_id = vehicle_id).update(
				old_driver_id = old_driver_id,
				new_driver_id = new_driver_id
			)

			Driver.objects.filter(user_id=new_driver_id).update(
				vehicle_id=vehicle_id,
				is_active = True
			)

			Driver.objects.filter(user_id=old_driver_id).update(
				vehicle_id=new_driver_vehicle_id,
				is_active = True
			)

			Vehicle.objects.filter(id=new_driver_vehicle_id).update(
				is_active = True
			)

			Vehicle.objects.filter(id=vehicle_id).update(
				is_active = True
			)
		else:
			print("Hello")
			VehicleAssingedToDriver.objects.create(
				vehicle_id_id = vehicle_id,
				old_driver_id = old_driver_id,
				new_driver_id = new_driver_id
			)

			Driver.objects.filter(user_id=new_driver_id).update(
				vehicle_id=vehicle_id,
				is_active = True
			)

			Driver.objects.filter(user_id=old_driver_id).update(
				vehicle_id=new_driver_vehicle_id,
				is_active = True
			)

			Vehicle.objects.filter(id=new_driver_vehicle_id).update(
				is_active = True
			)

			Vehicle.objects.filter(id=vehicle_id).update(
				is_active = True
			)



		return Response({'message', "vehicle assigned successfully !"})


from functools import reduce
from operator import and_
from django.db.models import Q
# from logistics_project.pagination import CustomPagination
from logistics_project.pagination import CustomPagination
class DriverRideHistoryAPI(APIView):
     def get(self, request):
        search_key = request.query_params.get('search_key') 
        query_filters = []
        
        bookingDetail = BookingDetail.objects.filter(driver_id=request.query_params['driver_id']).order_by('-id').values(
            'id','order_id', 'total_amount','trip_option', 'order__user__first_name', 'order__user__last_name', 'order__user__mobile_number', 'status__status_name','status__colour', 'travel_details', 'order__total_estimated_cost',
            'ordered_time','pickedup_time','order_accepted_time','canceled_time','order_droped_time', 'driver_id', 'order__user__profile_image', 'assigned','order__location_detail'
        )

        if search_key:
            filter_query = (
                Q(order__user__first_name__istartswith=search_key) |
                Q(order__user__mobile_number__istartswith=search_key) |
                Q(trip_option__istartswith=search_key) |
                Q(status__status_name__istartswith=search_key) |
                Q(order__total_estimated_cost__istartswith=search_key)
            )

            # Check if search_key is numeric and add the filter for order_id if it is
            if search_key.isdigit():
                filter_query |= Q(order_id=search_key)

            query_filters.append(filter_query)
        
        if query_filters:
            print('inside if')
            combined_query = reduce(and_, query_filters)
            bookingDetail = bookingDetail.filter(combined_query)
            
        for i in list(bookingDetail):
            if i['total_amount'] is not None:
                i['total_amount'] = round(float(i['total_amount']), 1)

            if UserFeedback.objects.filter(Q(driver_id=request.query_params['driver_id']) & Q(order_id=i['order_id']) & Q(rating_given_by="user")).exists():
                user_feedback_obj = UserFeedback.objects.filter(Q(driver_id=request.query_params['driver_id']) & Q(order_id=i['order_id']) & Q(rating_given_by="user")).values()
                for j in list(user_feedback_obj):
                    if i['driver_id'] == j['driver_id']:
                        i['ratings'] = j['rating']

            elif i['status__status_name'] == 'Trip Ended':
                i['ratings'] = None		

        for item in  bookingDetail:
                booking_id = item.get('id')	
                scheduledOrder = ScheduledOrder.objects.filter(booking=booking_id)
                for i in scheduledOrder:
                    item['scheduled_date_and_time'] = i.scheduled_date_and_time	
        
        # paginator = CustomPagination()
        # paginated_results = paginator.paginate_queryset(bookingDetail, request)
        # print('pagination results',paginated_results)
        # return paginator.get_paginated_response({'message': 'your orders are', 'data':paginated_results})

        # return Response({'message': 'your orders are', 'data':bookingDetail})
        paginator = CustomPagination()
        if 'page' in request.query_params:
            paginated_results = paginator.paginate_queryset(bookingDetail, request)
            return paginator.get_paginated_response({'message': 'your orders are', 'data': paginated_results})
        else:
            return Response({'message': 'your orders are', 'data': bookingDetail})


		
import requests
class CalculateETA(APIView):
    def calculate_distance_eta(self, origin_lat, origin_lng, dest_lat, dest_lng):
        # Make request to Google Maps Distance Matrix API for distance and ETA
        response = requests.get(
            f"https://maps.googleapis.com/maps/api/distancematrix/json",
            params={
                "origins": f"{origin_lat},{origin_lng}",
                "destinations": f"{dest_lat},{dest_lng}",
                "key": "AIzaSyBOYh5wDV6N5l0FLqfwZI_HgtBJ9TiiPss"
            }
        )
        distance_data = response.json()

        # Extract ETA (in seconds) from the response
        if "rows" in distance_data and distance_data["rows"]:
            elements = distance_data["rows"][0]["elements"]
            if elements and "duration" in elements[0]:
                eta_second = elements[0]["duration"]["value"]
                eta_seconds = eta_second / 60  # Convert ETA from seconds to minutes
                return round(eta_seconds, 2)  # Round off to two decimal places

        # Return None if no data found
        return None

    def get(self, request):
        # Get origin latitude and longitude from query parameters
        origin_latitude = float(request.query_params.get('origin_latitude'))
        origin_longitude = float(request.query_params.get('origin_longitude'))

        # Get destination latitude and longitude from query parameters
        dest_latitude = float(request.query_params.get('dest_latitude'))
        dest_longitude = float(request.query_params.get('dest_longitude'))
        
        # Calculate ETA between origin and destination
        eta_seconds = self.calculate_distance_eta(origin_latitude, origin_longitude, dest_latitude, dest_longitude)
        
        if eta_seconds is not None:
            response_data = {
                "origin_latitude": origin_latitude,
                "origin_longitude": origin_longitude,
                "dest_latitude": dest_latitude,
                "dest_longitude": dest_longitude,
                "eta_seconds": eta_seconds
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Unable to calculate ETA"}, status=status.HTTP_400_BAD_REQUEST)
    # def calculate_distance_eta(self, origin_lat, origin_lng, dest_lat, dest_lng):
    #     # Make request to Google Maps Distance Matrix API for distance and ETA
    #     response = requests.get(
    #         f"https://maps.googleapis.com/maps/api/distancematrix/json",
    #         params={
    #             "origins": f"{origin_lat},{origin_lng}",
    #             "destinations": f"{dest_lat},{dest_lng}",
    #             "key": "AIzaSyBOYh5wDV6N5l0FLqfwZI_HgtBJ9TiiPss"
    #         }
    #     )
    #     distance_data = response.json()

    #     # Extract ETA (in seconds) from the response
    #     if "rows" in distance_data and distance_data["rows"]:
    #         elements = distance_data["rows"][0]["elements"]
    #         if elements and "duration" in elements[0]:
    #             eta_seconds = elements[0]["duration"]["value"]
    #             print('eta-seconds',eta_seconds/60)
    #             return eta_seconds

    #     # Return None if no data found
    #     return None

    # def get(self, request):
    #     # Get origin latitude and longitude from query parameters
    #     origin_latitude = float(request.query_params.get('origin_latitude'))
    #     origin_longitude = float(request.query_params.get('origin_longitude'))

    #     # Get destination latitude and longitude from query parameters
    #     dest_latitude = float(request.query_params.get('dest_latitude'))
    #     dest_longitude = float(request.query_params.get('dest_longitude'))
        
    #     # Calculate ETA between origin and destination
    #     eta_seconds = self.calculate_distance_eta(origin_latitude, origin_longitude, dest_latitude, dest_longitude)
        
    #     if eta_seconds is not None:
    #         response_data = {
    #             "origin_latitude": origin_latitude,
    #             "origin_longitude": origin_longitude,
    #             "dest_latitude": dest_latitude,
    #             "dest_longitude": dest_longitude,
    #             "eta_seconds": eta_seconds
    #         }
    #         return Response(response_data, status=status.HTTP_200_OK)
    #     else:
    #         return Response({"error": "Unable to calculate ETA"}, status=status.HTTP_400_BAD_REQUEST)