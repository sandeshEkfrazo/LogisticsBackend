#-----------import----------
from django.conf import settings
from django.db.models import base
from django.db.utils import IntegrityError
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
# from requests import api
from rest_framework.response import Response
from requests.api import head, request
from userModule.views import *  
# import time
# import datetime
from django.utils.decorators import method_decorator
from logisticsapp.decorator import *
import requests
import uuid

import random
import json
import inspect
from django.core.mail import message, send_mail, EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.http import HttpResponsePermanentRedirect
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.serializers import Serializer
from .models import *
import jwt
from django.db.models import Q

from rest_framework import serializers
from rest_framework import generics,viewsets, status
from django.contrib import auth
from .serializers import *
from rest_framework import viewsets, status
from logisticsapp.backends import *
from rest_framework.authtoken.views import ObtainAuthToken

import re
from mimetypes import guess_extension
from django.conf import settings
import base64
import time
# import datetime
from datetime import datetime
import pandas as pd

from django.urls import reverse
import requests
import razorpay

class RegistrationApiVew(APIView):
    def post(self,request):
        data = request.data
        response = {}

        role_id=data.get('role_id')
        city_id=data.get('city_id')

        first_name=data.get('first_name')
        last_name=data.get('last_name')
        mobile_number=data.get('mobile_number')
        alternate_number=data.get('alternate_number')
        email=data.get('email')
        company_name=data.get('company_name')
        address=data.get('address')
        adhar_card=data.get('adhar_card')
        zip_code=data.get('zip_code')
        password= data.get('password')
        profile_image =data.get('profile_image')

        pan_card =data.get('pan_card')
        pan_card_image =data.get('pan_card_image')


        user_role = UserRoleRef.objects.get(id=role_id)
        username = email + user_role.user_role_name
        response_result = {}
        response_result['result'] = {}
        if data:
            if CustomUser.objects.filter(Q(mobile_number=mobile_number) ).exists():
                return Response({'error':'User already exists with same mobile_number'}, status= status.HTTP_409_CONFLICT)
            else:
                create_user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
                CustomUser.objects.create(mobile_number=mobile_number, user_id=create_user.id)

                # profile image
                if pan_card_image != '':
                    user_details = User.objects.get(id=create_user.id)
                    user_name = str(user_details.first_name)+str(random.randint(0,1000))
                    # print(pan_card_image,'pan_card_image')
                    split_base_url_data=pan_card_image.split(';base64,')[1]
                    # print(split_base_url_data,'split_base_url_data')
                    imgdata1 = base64.b64decode(split_base_url_data)

                    data_split = pan_card_image.split(';base64,')[0]
                    extension_data = re.split(':|;', data_split)[1]
                    guess_extension_data = guess_extension(extension_data)

                    # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data

                    # filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/pancard/"+user_name+guess_extension_data
                    filename1 = "/logistics/site/public/media/driving_license_file/"+user_name+guess_extension_data

                    image_name = user_name+guess_extension_data
                    ss=  open(filename1, 'wb')
                    # print(ss)
                    ss.write(imgdata1)
                    ss.close()

                if pan_card_image != '':
                    user_create = CustomUser.objects.create(
                        user_id = create_user.id,
                        role_id = role_id,
                        city_id = city_id,
                        first_name = first_name,
                        last_name = last_name,
                        mobile_number = mobile_number,
                        alternate_number = alternate_number,
                        email = email,
                        company_name = company_name,
                        address = address,
                        adhar_card = adhar_card,
                        zip_code = zip_code,
                        pan_card_base64=pan_card_image
                        )
                    if pan_card_image:
                        # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                        # user_create.pan_image_path = 'http://127.0.0.1:8000/media/pancard/'+ (str(image_name))
                        user_create.pan_image_path = 'https://logistics.thestorywallcafe.com/media/pancard/'+ (str(image_name))
                        
                        user_create.save()



                    if profile_image != '':


                        user_details = User.objects.get(id=create_user.id)
                        user_name = str(user_details.first_name)+str(random.randint(0,1000))
                        split_base_url_data=profile_image.split(';base64,')[1]
                        # print(split_base_url_data,'split_base_url_data')
                        imgdata1 = base64.b64decode(split_base_url_data)

                        data_split = profile_image.split(';base64,')[0]
                        extension_data = re.split(':|;', data_split)[1]
                        guess_extension_data = guess_extension(extension_data)

                        # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                        # filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/profile/"+user_name+guess_extension_data
                        filename1 = "/logistics/site/public/media/profile/"+user_name+guess_extension_data
                        image_name = user_name+guess_extension_data
                        ss=  open(filename1, 'wb')
                        # print(ss)
                        ss.write(imgdata1)
                        ss.close()

                    if profile_image != '':


                        user_create = CustomUser.objects.create(
                            user_id = create_user.id,
                            role_id = role_id,
                            city_id = city_id,
                            first_name = first_name,
                            last_name = last_name,
                            mobile_number = mobile_number,
                            alternate_number = alternate_number,
                            email = email,
                            company_name = company_name,
                            address = address,
                            adhar_card = adhar_card,
                            zip_code = zip_code,
                            base64=profile_image
                            )
                    if profile_image:
                        # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                        # user_create.profile_image_path = 'http://127.0.0.1:8000/media/profile/'+ (str(image_name))
                        user_create.profile_image_path = 'https://logistics.thestorywallcafe.com/media/profile/'+ (str(image_name))
                        user_create.save()


                    else:
                        # print('in else')
                        user_create = CustomUser.objects.create(
                            user_id = create_user.id,
                            role_id = role_id,
                            city_id = city_id,
                            first_name = first_name,
                            last_name = last_name,
                            mobile_number = mobile_number,
                            alternate_number = alternate_number,
                            email = email,
                            company_name = company_name,
                            address = address,
                            adhar_card = adhar_card,
                            zip_code = zip_code,
                            base64=profile_image,
                            pan_card=pan_card,
                            pan_card_base64=pan_card_image
                            )
                        auth_token = jwt.encode(
                                    {'user_id': create_user.id, 'role_id': user_create.role_id, 'city_id': user_create.city_id,
                                    }, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                        authorization = 'Bearer'+' '+auth_token

                        response_result = {}
                        response_result['result'] = {
                            'result': {'data': 'Register successful',
                            'token':authorization,
                            'user_id':create_user.id,
                            'custom_user_id':user_create.id,
                            'role_id':user_role.id,
                            'username':first_name,
                            'email':user_create.email
                            }}
                        response['Authorization'] = authorization
                        response['status'] = status.HTTP_200_OK
                        return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)


                    if (user_role.user_role_name == 'DRIVER'):
                        driver_driving_license=data.get('driver_driving_license')
                        badge=data.get('badge')

                        vehicle_name=data.get('vehicle_name')
                        vehicle_number=data.get('vehicle_number')
                        owner_id=data.get('owner_id') # string If Owner is a driver, then owner_ID is -1
                        license_status=data.get('license_status')
                        subcription=data.get('subcription_id')
                        driver_status =data.get('driver_status')
                        vehicle_status =data.get('vehicle_status')
                        license_expire_date =data.get('license_expire_date')
                        permit_expire_date =data.get('permit_expire_date')
                        fitness_certificate_expire_date =data.get('fitness_certificate_expire_date')
                        emission_test_expire_date =data.get('emission_test_expire_date')
                        insurence_expire_date =data.get('insurence_expire_date')
                        rc_expire_date =data.get('rc_expire_date')

                        get_days = Subscription.objects.get(id=subcription)
                        vsd = datetime.now()
                        ved = pd.to_datetime(str(vsd)) + pd.DateOffset(days=int(get_days.validity_period))
                        # print(vsd,'vsd split time')
                        # print(ved,'ved split time')
                        start1 = str(vsd).split(".")[0]
                        end1 = str(ved).split(".")[0]
                        # print(start1,'start1 split time')
                        # print(end1,'end1 split time')
                        validity_start_date_time = time.mktime(datetime.strptime(str(start1), "%Y-%m-%d %H:%M:%S").timetuple())
                        # print(validity_start_date_time,'validity_start_date_time timestamp')
                        validity_end_date_time = time.mktime(datetime.strptime(str(end1), "%Y-%m-%d %H:%M:%S").timetuple())
                        # print(validity_end_date_time,'validity_end_date_time timestamp')

                        user_details = User.objects.get(id=create_user.id)


                        user_name = str(user_details.first_name)+str(random.randint(0,1000))

                        driving_license_image=data.get('driving_license_image')

                        split_base_url_data=driving_license_image.split(';base64,')[1]
                        imgdata1 = base64.b64decode(split_base_url_data)

                        data_split = driving_license_image.split(';base64,')[0]
                        extension_data = re.split(':|;', data_split)[1]
                        guess_extension_data = guess_extension(extension_data)

                        # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                        # filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/driving_license/"+user_name+guess_extension_data
                        filename1 = "/logistics/site/public/media/driving_license_file/"+user_name+guess_extension_data
                        image_name = user_name+guess_extension_data
                        ss=  open(filename1, 'wb')
                        # print(ss)
                        ss.write(imgdata1)
                        ss.close()
                        vehicle_create = Vehicle.objects.create(vehicle_name=vehicle_name,vehicle_number=vehicle_number,)
                        driver_data = Driver.objects.create(
                            driver_driving_license = driver_driving_license,
                            badge = badge,
                            user_id = create_user.id,
                            vehicle_id = vehicle_create.id,
                            owner_id = owner_id,
                            base64=driving_license_image,
                            subcription_id=subcription,

                            license_status=license_status,
                            validity_start_date_time=validity_start_date_time,
                            validity_end_date_time=validity_end_date_time,
                            driver_status = driver_status,
                            vehicle_status = vehicle_status,
                            license_expire_date = license_expire_date,
                            permit_expire_date = permit_expire_date,
                            fitness_certificate_expire_date = fitness_certificate_expire_date,
                            emission_test_expire_date = emission_test_expire_date,
                            insurence_expire_date = insurence_expire_date,
                            rc_expire_date = rc_expire_date,
                        )


                        response_result['result']['driver_driving_license']=  driver_data.driver_driving_license,
                        response_result['result']['badge']    = driver_data.badge,
                        response_result['result']['user_id']   = driver_data.user_id,
                        response_result['result']['vehicle_id']  = driver_data.vehicle_id,
                        response_result['result']['owner']    = driver_data.owner_id,


                    if driving_license_image:
                        course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                        driver_data.driving_license_image_path = 'http://127.0.0.1:8000/media/driving_license/'+ (str(image_name))
                    if driving_license_image:
                        driver_data.driving_license_image_path = 'https://logistics.thestorywallcafe.com/media/driving_license_file/'+ (str(image_name))
                        driver_data.save()

                        # auth_token = jwt.encode(
                        #             {'user_id': create_user.id, 'role_name':user_role.user_role_name,'role_id': user_create.role_id, 'city_id': user_create.city_id,
                        #             }, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                        # authorization = 'Bearer'+' '+auth_token


                        response_result['result'] = {
                            'result': {'data': 'Register successful',
                            'token':authorization,
                            'user_id':create_user.id,
                            'custom_user_id':user_create.id,
                            'role_id':user_create.role_id,
                            'role_name':user_role.user_role_name,
                            'username':first_name,
                            'email':user_create.email
                            }}
                        response['Authorization'] = authorization
                        response['status'] = status.HTTP_200_OK
                        return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)


                    else:
                        return Response({'error':'Please fill all the details'})
        


class LoginView(APIView):
    def post(self, request):
        response = {}
        data = request.data
        username = data.get('username')
        password = data.get('password')
        role_id = data.get('role_id')
        user_role = UserRoleRef.objects.get(id=role_id)

        username = username + user_role.user_role_name

        user_check = User.objects.get(username= username)

        if user_check:
            user = auth.authenticate(username=username, password=password)

            if user:
                user_data = User.objects.get(id=user.id)
                c_user = CustomUser.objects.get(user_id=user.id)

                # auth_token = jwt.encode(
                #     {'user_id': user.id, 'username': user.first_name, 'email': user.email,'role_name':user_role.user_role_name,'role_id':c_user.role_id,}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                authorization = 'Bearer'+' '+auth_token
                response_result = {}
                response_result['result'] = {
                    'detail': 'Login successfull',
                    'user_id':user_data.id,
                    'custom_user_id':c_user.id,
                    'username':user_data.first_name,
                    'email':user_data.email,
                    'role_id':c_user.role_id,
                    'role_name':user_role.user_role_name,
                    'token':authorization,
                    'status': status.HTTP_200_OK}
                response['Authorization'] = authorization
                response['status'] = status.HTTP_200_OK
                # return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)


            else:
                header_response = {}
                response['error'] = {'error': {
                    'detail': 'Invalid Username / Password', 'status': status.HTTP_401_UNAUTHORIZED}}
                return Response(response['error'], headers=header_response,status= status.HTTP_401_UNAUTHORIZED)

            return Response(response_result, headers=response,status= status.HTTP_200_OK)
        else:

            response['error'] = {'error': {
                    'detail': 'Invalid Username / Password', 'status': status.HTTP_401_UNAUTHORIZED}}
            return Response(response['error'], status= status.HTTP_401_UNAUTHORIZED)


class SignUpPhoneNumberApiView(APIView):
    def post(self,request):
        data = request.data

        mobile_number = data.get('mobile_number')
        user_role_name = data.get('user_role_name')
        if UserRoleRef.objects.filter(Q(user_role_name=user_role_name)).exists():
            user_role = UserRoleRef.objects.get(user_role_name=user_role_name)
            otp = random.randint(100000, 999999)

            # user_role_ref_data = UserRoleRef.objects.create(user_role_name=user_role_name)

            if CustomUser.objects.filter(Q(mobile_number=mobile_number)).exists():
                return Response({'error':{'message':'User have  already registered'}}, status=status.HTTP_406_NOT_ACCEPTABLE)
            

            else:
                sendMobileOTp(mobile_number)
                store_otp = CustomUser.objects.create(mobile_number=mobile_number,reset_otp=int(otp),
                role_id = user_role.id 
                )
                
                data_dict = {}
                data_dict["OTP"] = otp
            
                auth_token = jwt.encode(
                                    {'user_id': store_otp.id, 'user_role_name':user_role_name,
                                    'role_id': user_role.id,'mobile_number':mobile_number,'otp':otp

                                    }, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                # print(auth_token,'this is auth_token')
                authorization = 'Bearer'+' '+auth_token

                response_result = {}
                response = {}
                response_result['result'] = {
                            'result': {'data': 'Register successful',
                            'token':authorization,
                            'user_id':store_otp.id,
                            "mobile_number":mobile_number,
                            "user_role_name":user_role_name,
                            # 'email':user_create.email,
                            'role_id': user_role.id,
                            'otp':otp
                            # 'result':data_dict
                            
                            }}
                response['Authorization'] = authorization
                response['status'] = status.HTTP_200_OK
                return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)
        else:
            return Response({'error':{'message':'UserRole  doesnot exists'}})

class LoginApiView(APIView):
    def post(self,request):
        data = request.data

        mobile_number = data.get('mobile_number')
            
        user_role_name = data.get('user_role_name')

        role = UserRoleRef.objects.get(Q(user_role_name=user_role_name))
       
        otp = random.randint(100000, 999999)
        response = {}
        
        if CustomUser.objects.filter(Q(mobile_number=mobile_number) & Q(role__user_role_name=user_role_name)).exists():
            sendMobileOTp(mobile_number)
            # print("CustomUser")
            cuser = CustomUser.objects.get(Q(mobile_number=mobile_number) & Q(role__user_role_name=user_role_name))
            store_otp = CustomUser.objects.filter(id=cuser.id, role__user_role_name=user_role_name).update(reset_otp=int(otp))
            data_dict = {}
            # data_dict["OTP"] = otp  

            if cuser:
                                    
                auth_token = jwt.encode(
                    {'user_id': cuser.id, 'username': cuser.first_name, 'email': cuser.email,'role_name':user_role_name,'role_id':cuser.role_id,}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
                authorization = 'Bearer'+' '+auth_token
                response_result = {}
                response = {}
                response_result['result'] = {
                    'detail': 'Login successfull',

                    'cuser_id':cuser.id,
                    "mobile_number":mobile_number,
                    
                    'user_role_name':user_role_name,
                    
                    'role_id':role.id,
                    'otp':otp,
                    'token':authorization,
                    'status': status.HTTP_200_OK
                    }
                response['Authorization'] = authorization
                response['status'] = status.HTTP_200_OK
                return Response(response_result['result'], headers=response,status= status.HTTP_200_OK)

            else:
                header_response = {}
                response['error'] = {'error': {
                    'detail': 'Invalid Username / Password', 'status': status.HTTP_401_UNAUTHORIZED}}
                return Response(response['error'], headers=header_response,status= status.HTTP_401_UNAUTHORIZED)
        else:      
            response['error'] = {'error': {
                    'detail': 'Invalid Username / Password', 'status': status.HTTP_401_UNAUTHORIZED}}
            return Response(response['error'], status= status.HTTP_401_UNAUTHORIZED)

class VerifyOtpPhoneNumberApiView(APIView):
    def post(self, request):
        data = request.data
        otp_recieved = data.get('otp')
        mobile_number= data.get('mobile_number')
        user_role_name = data.get('user_role_name')


        role = UserRoleRef.objects.get(Q(user_role_name=user_role_name))
        
        print("role id",role.id, CustomUser.objects.filter(Q(mobile_number=mobile_number) & Q(role_id=role.id)).exists())
        if  CustomUser.objects.filter(Q(mobile_number=mobile_number) & Q(role_id=role.id)).exists():
            res = verifyOTP(mobile_number, otp_recieved)
            print("response==>>", res)
            return Response(res)
        else:
            return Response({'error':{'message': 'Unauthorized!'}})



class SignupUserApiView(APIView):
    def post(self, request):
        data = request.data

        first_name  =data.get('first_name')
        last_name =data.get('last_name')
        company_name =data.get('company_name')
        mobile_number=data.get('mobile_number')
        email =data.get('email')
        whatsup_number =data.get('whatsup_number')


        if  CustomUser.objects.filter(Q(mobile_number=mobile_number)).exists():
            
            user_check = CustomUser.objects.filter(mobile_number=mobile_number).update(
                first_name=first_name,
                last_name=last_name,
                company_name=company_name,
                email=email,
                whatsup_number=whatsup_number,)
            
            return Response({'result':{'message': 'User Created!'}})
        else:

            return Response({'error':{'message': 'Your not registered user, please register!'}})



class SignUpforDriverOrOwner(APIView):
    def post(self, request):
        data = request.data

        # Customuser User
        user_role_name = data.get('user_role_name')
        

        first_name=data.get('first_name')
        mobile_number=data.get('mobile_number')
        
        adhar_card_front_side_img=data.get('adhar_card_front_side_img')
        adhar_card_back_side_img=data.get('adhar_card_back_side_img')


        # adhar_card_front_side_img_path=data.get('adhar_card_front_side_img_path')

        
        # adhar_card_back_side_img_path=data.get('adhar_card_back_side_img_path')

        # Driver details
        driver_driving_license=data.get('driver_driving_license_number')
        badge=data.get('badge')

        registration_certificate_front_side_img=data.get('registration_certificate_front_side_img')
        registration_certificate_back_side_img=data.get('registration_certificate_back_side_img')
        
        pollution_certificate_front_side_img=data.get('pollution_certificate_front_side_img')


        # no mandatory
        fitness_certificate_front_side_img=data.get('fitness_certificate_front_side_img') 
        # no mandatory
        permit_front_side_img=data.get('permit_front_side_img')
        


        if UserRoleRef.objects.filter(Q(user_role_name=user_role_name)).exists():

            role = UserRoleRef.objects.get(Q(user_role_name=user_role_name))
        
            if CustomUser.objects.filter(Q(mobile_number=mobile_number) & Q(role_id=role.id) ).exists():


                user_details = CustomUser.objects.get(Q(mobile_number=mobile_number) & Q(role_id=role.id))

                user_name = str(user_details.first_name)+str(random.randint(0,1000))

                    # Spliting the base64 image and get data 
                split_adhar_card_f_url_data = adhar_card_front_side_img.split(';base64,')[1]

                    # decode the base64 and store in varibale 
                imgdata1 = base64.b64decode(split_adhar_card_f_url_data)

                    # Getting the extension fron base64 image
                data_split = adhar_card_front_side_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)


                    # Save the file path in varibale

                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                adhar_card_front_side_img_filename1 = "/logistics/site/public/media/adhar_card/"+user_name+guess_extension_data
                adhar_card_front_path = "https://logistics.thestorywallcafe.com/media/adhar_card/"+user_name+guess_extension_data
                    # Open the empty file 
                ss =  open(adhar_card_front_side_img_filename1, 'wb')
                    # write the base64 data to that empty file
                ss.write(imgdata1)
                    # close the file
                ss.close()


                
                
                

                # adhar_card_back_side_img
                user_details = CustomUser.objects.get(Q(mobile_number=mobile_number) & Q(role_id=role.id))

                user_name = str(user_details.first_name)+str(random.randint(0,1000))

                    # Spliting the base64 image and get data 
                split_adhar_card_b_url_data = adhar_card_back_side_img.split(';base64,')[1]

                    # decode the base64 and store in varibale 
                imgdata1 = base64.b64decode(split_adhar_card_b_url_data)

                    # Getting the extension fron base64 image
                data_split = adhar_card_back_side_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)


                    # Save the file path in varibale

                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                adhar_card_back_side_img_filename = "/logistics/site/public/media/adhar_card/"+user_name+guess_extension_data
                adhar_card_back_path = "https://logistics.thestorywallcafe.com/media/adhar_card/"+user_name+guess_extension_data
                    # Open the empty file 
                ss =  open(adhar_card_back_side_img_filename, 'wb')
                    # write the base64 data to that empty file
                ss.write(imgdata1)
                    # close the file
                ss.close()




                # registration_certificate_front_side_img
                user_details = CustomUser.objects.get(Q(mobile_number=mobile_number) & Q(role_id=role.id))

                user_name = str(user_details.first_name)+str(random.randint(0,1000))

                    # Spliting the base64 image and get data 
                split_registration_certificate_front_url_data = registration_certificate_front_side_img.split(';base64,')[1]

                    # decode the base64 and store in varibale 
                imgdata1 = base64.b64decode(split_registration_certificate_front_url_data)

                    # Getting the extension fron base64 image
                data_split = adhar_card_front_side_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)


                    # Save the file path in varibale

                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                registration_certificate_front_side_img_filename = "/logistics/site/public/media/registration_certificate/"+user_name+guess_extension_data
                
                registration_certificate_front_side_path = "https://logistics.thestorywallcafe.com/media/registration_certificate/"+user_name+guess_extension_data
                    # Open the empty file 
                ss =  open(registration_certificate_front_side_img_filename, 'wb')
                ss.write(imgdata1)
                ss.close()



                # registration_certificate_back_side_img
                user_details = CustomUser.objects.get(Q(mobile_number=mobile_number) & Q(role_id=role.id))

                user_name = str(user_details.first_name)+str(random.randint(0,1000))

                    # Spliting the base64 image and get data 
                split_registration_certificate_back_side_url_data = registration_certificate_back_side_img.split(';base64,')[1]

                    # decode the base64 and store in varibale 
                imgdata1 = base64.b64decode(split_registration_certificate_back_side_url_data)

                    # Getting the extension fron base64 image
                data_split = adhar_card_front_side_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)


                    # Save the file path in varibale

                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                registration_certificate_back_side_img_filename = "/logistics/site/public/media/registration_certificate/"+user_name+guess_extension_data
                registration_certificate_back_side_path = "https://logistics.thestorywallcafe.com/media/registration_certificate/"+user_name+guess_extension_data
                    # Open the empty file 
                ss =  open(registration_certificate_back_side_img_filename, 'wb')
                ss.write(imgdata1)
                ss.close()

                # pollution_certificate_front_side_img

                user_details = CustomUser.objects.get(Q(mobile_number=mobile_number) & Q(role_id=role.id))

                user_name = str(user_details.first_name)+str(random.randint(0,1000))

                    # Spliting the base64 image and get data 
                pollution_certificate_front_side_img_url_data = pollution_certificate_front_side_img.split(';base64,')[1]

                    # decode the base64 and store in varibale 
                imgdata1 = base64.b64decode(pollution_certificate_front_side_img_url_data)

                    # Getting the extension fron base64 image
                data_split = adhar_card_front_side_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)


                    # Save the file path in varibale

                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                pollution_certificate_front_side_img_url_data_filename = "/logistics/site/public/media/pollution_certificate/"+user_name+guess_extension_data
                pollution_certificate_front_side_img_path = "https://logistics.thestorywallcafe.com/media/pollution_certificate/"+user_name+guess_extension_data
                    # Open the empty file 
                ss =  open(pollution_certificate_front_side_img_url_data_filename, 'wb')
                ss.write(imgdata1)
                ss.close()
               
                driver_data = Driver.objects.create(driver_driving_license=driver_driving_license,
                                badge=badge,fitness_certificate_front_side_img=fitness_certificate_front_side_img,
                                                    )

                vehicle_data = Vehicle.objects.create(registration_certificate_front_side_img_path=registration_certificate_front_side_path,
                                                        registration_certificate_back_side_img_path=registration_certificate_back_side_path,
                                                        
                                                        registration_certificate_front_side_img=registration_certificate_front_side_img,
                                                        registration_certificate_back_side_img=registration_certificate_back_side_img,

                                                        pollution_certificate_front_side_img=pollution_certificate_front_side_img,
                                                        pollution_certificate_front_side_img_path=pollution_certificate_front_side_img_path,

                                                        permit_front_side_img=permit_front_side_img,
                                                        )


                CustomUser.objects.filter(Q(mobile_number=mobile_number) & Q(role_id=role.id) ).update(
                    driver_id=driver_data.id,
                    vehicle_id=vehicle_data.id,
                    first_name = first_name,
                    #customer
                    adhar_card_front_side_img=adhar_card_front_side_img,
                    adhar_card_back_side_img=adhar_card_back_side_img,

                    # registration_certificate_front_side_img=registration_certificate_front_side_img,
                    # registration_certificate_back_side_img=registration_certificate_back_side_img,
                    # pollution_certificate_front_side_img=pollution_certificate_front_side_img,

                    adhar_card_front_side_img_path  =  adhar_card_front_path,
                    adhar_card_back_side_img_path = adhar_card_back_path,
                    
                    )

                if  fitness_certificate_front_side_img != ' ':

                    user_details = CustomUser.objects.get(Q(mobile_number=mobile_number) & Q(role_id=role.id))

                    user_name = str(user_details.first_name)+str(random.randint(0,1000))

                        # Spliting the base64 image and get data 
                    fitness_certificate_front_side_img_url_data = fitness_certificate_front_side_img.split(';base64,')[1]

                        # decode the base64 and store in varibale 
                    imgdata1 = base64.b64decode(fitness_certificate_front_side_img_url_data)

                        # Getting the extension fron base64 image
                    data_split = adhar_card_front_side_img.split(';base64,')[0]
                    extension_data = re.split(':|;', data_split)[1]
                    guess_extension_data = guess_extension(extension_data)


                        # Save the file path in varibale

                    # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                    fitness_certificate_front_side_img_url_data_filename = "/logistics/site/public/media/fitness_certificate/"+user_name+guess_extension_data
                    fitness_certificate_front_side_img_path = "https://logistics.thestorywallcafe.com/media/fitness_certificate/"+user_name+guess_extension_data
                        # Open the empty file 
                    ss =  open(fitness_certificate_front_side_img_url_data_filename, 'wb')
                    ss.write(imgdata1)
                    ss.close()
                    


                    Driver.objects.filter(Q(id=driver_data.id) ).update(
                        fitness_certificate_front_side_img_path=fitness_certificate_front_side_img_path,
                        fitness_certificate_front_side_img=fitness_certificate_front_side_img
                    
                    )

                if  permit_front_side_img != ' ':

                    user_details = CustomUser.objects.get(Q(mobile_number=mobile_number) & Q(role_id=role.id))

                    user_name = str(user_details.first_name)+str(random.randint(0,1000))

                        # Spliting the base64 image and get data 
                    permit_front_side_img_url_data = permit_front_side_img.split(';base64,')[1]

                        # decode the base64 and store in varibale 
                    imgdata1 = base64.b64decode(permit_front_side_img_url_data)

                        # Getting the extension fron base64 image
                    data_split = adhar_card_front_side_img.split(';base64,')[0]
                    extension_data = re.split(':|;', data_split)[1]
                    guess_extension_data = guess_extension(extension_data)


                        # Save the file path in varibale

                    # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                    permit_front_side_img_url_data_filename = "/logistics/site/public/media/permit_front_side/"+user_name+guess_extension_data
                    permit_front_side_img_path = "https://logistics.thestorywallcafe.com/media/permit_front_side/"+user_name+guess_extension_data
                        # Open the empty file 
                    ss =  open(permit_front_side_img_url_data_filename, 'wb')
                    ss.write(imgdata1)
                    ss.close()  

                    Vehicle.objects.filter(Q(id=vehicle_data.id) ).update(
                        permit_front_side_img_path=permit_front_side_img_path,
                        permit_front_side_img=permit_front_side_img
                    
                    )

       

                return Response({'result':{'message': 'Driver or Owner Created!'}})
 
            else:

                return Response({'error':{'error_message': 'User DoesNotExist!'}})
        else:


            return Response({'error':{'error_message': 'User role DoesNotExist!'}})




class ForgotPasswordSendOtp(APIView):

    def post(self, request):
        data = request.data

        username = data.get('username')
        otp = random.randint(100000, 999999)

        if User.objects.filter(Q(username=username)).exists():
            update_otp = CustomUser.objects.filter(email=username).update(reset_otp=int(otp))
            # print(update_otp,'update_otp')

        else:
            return Response({'error':{'message':'username doesnot exists'}})

        user_check=CustomUser.objects.get(email=username)
        email=user_check.email
        # print(email,'email')
        # if '@' in username:
        message = inspect.cleandoc('''Hi ,\n %s is your OTP to Forgot Password to your logistics account.\nThis OTP is valid for next 10 minutes,
                                \nWith Warm Regards,\nTeam Logistics,
                                ''' % (Otp))
        send_mail(
            'Greetings from EzTime', message
            ,
            'farhana@ekfrazo.in',
            [email],

        )
        data_dict = {}
        data_dict["OTP"] = Otp
        return Response({'result':data_dict})


class OtpVerificationForgotpass(APIView):

    def post(self, request):
        data = request.data
        otp = data.get('otp')
        user_id = data.get('user_id')
        user_check=CustomUser.objects.get(user_id=user_id)

        if otp==user_check.reset_otp:
            update_otp = CustomUser.objects.filter(user_id=user_id).update(reset_otp=None)
            return Response({'result':{'message': 'OTP matcheds successfully'}})
        else:
            return Response({'error':{'message': 'Invalid OTP'}})


class ForgotPasswordReset(APIView):

    def post(self, request):
        data = request.data

        username = data.get('username')
        password = data.get('password')
        user_check = User.objects.filter(username= username)
        if user_check:
            user_data = User.objects.get(username= username)
            user_data.set_password(password)
            user_data.save()
            message= 'Hello!\nYour password has been updated sucessfully. '
            subject= 'Password Updated Sucessfully '
            email = EmailMessage(subject, message, to=[user_data.email])
            email.send()
            return Response({'result':{'message': 'Password Updated Sucessfully'}})
        else:
            return Response({'error':{'message': 'Please Enter Valid username'}})


class ChangePassword(APIView):

    def post(self,request):
        data         =    request.data
        user_id        =    data.get('user_id')
        new_password        =    data.get('new_password')
        old_password        =    data.get('old_password')


        # print(data,'dattaaaaa')
        try:
            check_user = User.objects.get(id=user_id)
            if check_user:
                if check_user.check_password(old_password):
                    check_user.set_password(new_password)
                    check_user.save()
                    return Response({'result':'password changed successfully!'})
                else:
                    return Response({
                    'error':{'message':'incorrect old password!',
                    'status_code':status.HTTP_401_UNAUTHORIZED,
                    }},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error':{'message':'user does not exists!',
                    'status_code':status.HTTP_404_NOT_FOUND,
                    }},status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
                return Response({
                'error':{'message':'user does not exists!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)




# @method_decorator([AutorizationRequired], name='dispatch')
class UserRoleRefView(APIView):
    def get(self,request):
        # CheckAccess(request)
        data=request.data
        user_role_name=data.get('user_role_name')

        id = request.query_params.get('id')
        if id:
            all_data = UserRoleRef.objects.filter(id=id).values()
            # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})


        else:
            all_data = UserRoleRef.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})
    def post(self, request):
        data = request.data
        user_role_name = data.get('user_role_name')
        selected_page_no = 1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)

        try:
            emp_role, created = UserRoleRef.objects.get_or_create(user_role_name=user_role_name)

            if not created:
                # user_role_name already exists in the database
                return Response({
                    'error': {
                        'message': 'User role already exists',
                        'status_code': status.HTTP_400_BAD_REQUEST,
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            posts = UserRoleRef.objects.all().values()
            paginator = Paginator(posts, 10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({
                'result': {
                    'status': 'Created',
                    'data': list(page_obj),
                }
            })

        except IntegrityError as e:
            error_message = e.args
            return Response({
                'error': {
                    'message': 'DB error!',
                    'detail': error_message,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                }
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        data = request.data
        user_role_name=data.get('user_role_name')

        try:
            emp_role= UserRoleRef.objects.filter(id=pk).update(
                                        user_role_name=user_role_name,)



        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):

        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})


        all_values = UserRoleRef.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})



# @method_decorator([AutorizationRequired], name='dispatch')
class CityView(APIView):
    def get(self,request):
        data=request.data
        user_role_name=data.get('user_role_name')
        # CheckAccess(request)

        id = request.query_params.get('id')
        if id:
            all_data = City.objects.filter(id=id).values()
            # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})


        else:
            all_data = City.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        user_role_name=data.get('user_role_name')
        city_name=data.get('city_name')


        selected_page_no =1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)


        try:
            emp_role = City.objects.create(city_name=city_name,)


            posts = City.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        city_name=data.get('city_name')
        user_role_name=data.get('user_role_name')
        try:
            emp_role= City.objects.filter(id=pk).update(city_name=city_name,
                                            )



        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        data=request.data
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})


        all_values = City.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})

import os
import array as ar
# @method_decorator([AutorizationRequired], name='dispatch')
class VehicleTypesView(APIView):
    def get(self,request):
        data=request.data
        vehicle_type_image=data.get('vehicle_type_image')
        # vehicle_type_sub_images=data.get('vehicle_type_sub_images')
        id = request.query_params.get('id')
        if id:
            all_data = VehicleTypes.objects.filter(id=id).values()
            # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')
            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = VehicleTypes.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        vehicle_type_name=data.get('vehicle_type_name')
        capacity=data.get('capacity')
        size=data.get('size')
        details=data.get('details')
        per_km_price = data.get('per_km_price')
        min_charge = data.get('min_charge')
        max_time_min = data.get('max_time_min')
        badge = data.get('badge')
        per_min_price=data.get('per_min_price')
        vehicle_type_image=data.get('vehicle_type_image')
        vehicle_description=data.get('vehicle_description')
            # return Response({i})
        # converted_vehicle_type_image= vehicle_type_sub_images
        # vehicle_type_sub_images=converted_vehicle_type_image
        # vehicle_type_sub_images={}
        # converted_vehicle_type_sub_images=convertBase64(vehicle_type_image, 'vehicle_type_sub_images', size, "vehicle_type_image")
        selected_page_no =1
        page_number = request.GET.get('page')

        if page_number:
            selected_page_no = int(page_number)


        sub_image_list  = []
     
        for i in data.get('vehicle_type_sub_images'):
            # print(i,'ii')
            image_name = 'image'+str(random.randint(0,1000))
            sub_image_data = convertBase64(i['image'], image_name, size, "vehicle_type_image")
            sub_image_dic = {
                'image':sub_image_data
            }
            sub_image_list.append(sub_image_dic)

        vehicle_type_discription_list=[]
        descriptions=vehicle_description
        vehicle_description_dict={
            'description':descriptions
        }
        # description=vehicle_type_discription_dict

        # for i in data.get('vehicle_description'):
            # descriptions=vehicle_description
        # vehicle_description_dict=vehicle_description
        
        vehicle_type_discription_list.append(vehicle_description_dict)

        converted_vehicle_type_image = convertBase64(vehicle_type_image, 'vehicle_type_image', size, "vehicle_type_image")
        try:
            VehicleTypes.objects.create(
                                            vehicle_type_name=vehicle_type_name,
                                            capacity=capacity,
                                            size=size,
                                            details=details,
                                            per_km_price=per_km_price,
                                            min_charge = min_charge,
                                            max_time_min = max_time_min,
                                            per_min_price=per_min_price,
                                            badge = badge,
                                            vehicle_type_image=converted_vehicle_type_image,
                                            vehicle_type_sub_images=sub_image_list,
                                            vehicle_description=vehicle_type_discription_list,
                                            )

            posts = VehicleTypes.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)


    def put(self,request,pk):
        # CheckAccess(request)
        data = request.data
        # if data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        vehicle_type_name=data.get('vehicle_type_name')
        capacity=data.get('capacity')
        size=data.get('size')
        details=data.get('details')
        min_charge = data.get('min_charge')
        max_time_min = data.get('max_time_min')
        badge = data.get('badge')
        per_min_price=data.get('per_min_price')
        time=data.get('time')
        vehicle_type_image=data.get('vehicle_type_image')
        vehicle_description=data.get('vehicle_description')
        # vehicle_type_sub_images=data.get('vehicle_type_sub_images')
        converted_vehicle_type_image = convertBase64(vehicle_type_image, 'vehicle_type_image', size, "vehicle_type_image")

        
        sub_image_list  = []
     
        for i in data.get('vehicle_type_sub_images'):
            # print(i,'ii')
            image_name = 'image'+str(random.randint(0,1000))
            sub_image_data = convertBase64(i['image'], image_name, size, "vehicle_type_image")
            sub_image_dic = {
                'image':sub_image_data
            }
            sub_image_list.append(sub_image_dic)

        vehicle_type_discription_list=[]
        # vehicle_type_discription_dict={}

        descriptions=vehicle_description
        vehicle_description_dict={
            'description':descriptions
        }
        vehicle_type_discription_list.append(vehicle_description_dict)
        # converted_vehicle_type_sub_images=convertBase64(vehicle_type_image, 'vehicle_type_sub_images', size, "vehicle_type_image")
        try:


            VehicleTypes.objects.filter(id=pk).update(
                vehicle_type_name=vehicle_type_name,
                capacity=capacity,
                size=size,
                min_charge = min_charge,
                max_time_min = max_time_min,
                per_min_price=per_min_price,
                badge = badge,
                vehicle_type_image=converted_vehicle_type_image,
                vehicle_type_sub_images=sub_image_list,
                vehicle_description=vehicle_type_discription_list,
                )

            Driver.objects.filter(id=pk).update(
                time=time,
            )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})

        all_values = VehicleTypes.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        # index=[]
        # if i in index:
        #     index_val=index.pop(i)
            # print(index_val)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})

@method_decorator([AutorizationRequired], name='dispatch')
class CustomUserView(APIView):
    def get(self,request):
        CheckAccess(request)
        id = request.query_params.get('id')
        if id:
            all_data = CustomUser.objects.filter(id=id).values()
            # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})
        else:
            all_data = CustomUser.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        CheckAccess(request)
        data = request.data
        user=data.get('user_id')
        role=data.get('role_id')
        city=data.get('city_id')
        first_name=data.get('first_name')
        last_name=data.get('last_name')
        email=data.get('email')
        company_name=data.get('company_name')
        mobile_number=data.get('mobile_number')
        alternate_number=data.get('alternate_number')
        zip_code=data.get('zip_code')
        address=data.get('address')
        adhar_card=data.get('adhar_card')

        profile_image =data.get('profile_image')
        if profile_image != '':
            user_details = User.objects.get(id=user_id)
            user_name = str(user_details.first_name)+str(random.randint(0,1000))
            split_base_url_data=profile_image.split(';base64,')[1]
            # print(split_base_url_data,'split_base_url_data')
            imgdata1 = base64.b64decode(split_base_url_data)

            data_split = profile_image.split(';base64,')[0]
            extension_data = re.split(':|;', data_split)[1]
            guess_extension_data = guess_extension(extension_data)

            # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
            filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/profile/"+user_name+guess_extension_data
            image_name = user_name+guess_extension_data
            ss=  open(filename1, 'wb')
            # print(ss)
            ss.write(imgdata1)
            ss.close()

            selected_page_no =1
            page_number = request.GET.get('page')
            if page_number:
                selected_page_no = int(page_number)
            try:
                user_create = CustomUser.objects.create(
                                                user_id=user,
                                                role_id=role,
                                                city_id=city,
                                                first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                company_name=company_name,
                                                mobile_number=mobile_number,
                                                alternate_number=alternate_number,
                                                zip_code=zip_code,
                                                address=address,
                                                adhar_card=adhar_card,
                                                base64=profile_image,

                                                )

                if profile_image:
                        # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                        user_create.profile_image_path = 'http://127.0.0.1:8000/media/profile/'+ (str(image_name))
                        user_create.save()

                posts = CustomUser.objects.all().values()
                paginator = Paginator(posts,10)
                try:
                    page_obj = paginator.get_page(selected_page_no)
                except PageNotAnInteger:
                    page_obj = paginator.page(1)
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)
                return Response({'result':{'status':'Created','data':list(page_obj)}})

            except IntegrityError as e:
                error_message = e.args
                return Response({
                'error':{'message':'DB error!',
                'detail':error_message,
                'status_code':status.HTTP_400_BAD_REQUEST,
                }},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user_create = CustomUser.objects.create(
                                                user_id=user,
                                                role_id=role,
                                                city_id=city,
                                                first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                company_name=company_name,
                                                mobile_number=mobile_number,
                                                alternate_number=alternate_number,
                                                zip_code=zip_code,
                                                address=address,
                                                adhar_card=adhar_card,
                                                )


                posts = CustomUser.objects.all().values()
                paginator = Paginator(posts,10)
                try:
                    page_obj = paginator.get_page(selected_page_no)
                except PageNotAnInteger:
                    page_obj = paginator.page(1)
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)
                return Response({'result':{'status':'Created','data':list(page_obj)}})

            except IntegrityError as e:
                error_message = e.args
                return Response({
                'error':{'message':'DB error!',
                'detail':error_message,
                'status_code':status.HTTP_400_BAD_REQUEST,
                }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        user=data.get('user_id')
        role=data.get('role_id')
        city=data.get('city_id')
        first_name=data.get('first_name')
        last_name=data.get('last_name')
        email=data.get('email')
        company_name=data.get('company_name')
        mobile_number=data.get('mobile_number')
        alternate_number=data.get('alternate_number')
        zip_code=data.get('zip_code')
        address=data.get('address')
        adhar_card=data.get('adhar_card')

        profile_image =data.get('profile_image')
        if profile_image != '':
            user_details = User.objects.get(id=user_id)
            user_name = str(user_details.first_name)+str(random.randint(0,1000))
            split_base_url_data=profile_image.split(';base64,')[1]
            # print(split_base_url_data,'split_base_url_data')
            imgdata1 = base64.b64decode(split_base_url_data)

            data_split = profile_image.split(';base64,')[0]
            extension_data = re.split(':|;', data_split)[1]
            guess_extension_data = guess_extension(extension_data)

            # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
            filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/profile/"+user_name+guess_extension_data
            image_name = user_name+guess_extension_data
            ss=  open(filename1, 'wb')
            # print(ss)
            ss.write(imgdata1)
            ss.close()

            selected_page_no =1
            page_number = request.GET.get('page')
            if page_number:
                selected_page_no = int(page_number)

            try:
                CustomUser.objects.filetr(user_id=user,).update(
                                                user_id=user,
                                                role_id=role,
                                                city_id=city,
                                                first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                company_name=company_name,
                                                mobile_number=mobile_number,
                                                alternate_number=alternate_number,
                                                zip_code=zip_code,
                                                address=address,
                                                adhar_card=adhar_card,
                                                base64=profile_image,

                                                )
                user_get = CustomUser.objects.get(user_id=user,)
                if profile_image:
                        # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                        user_get.profile_image_path = 'http://127.0.0.1:8000/media/profile/'+ (str(image_name))
                        user_get.save()


                posts = CustomUser.objects.all().values()
                paginator = Paginator(posts,10)
                try:
                    page_obj = paginator.get_page(selected_page_no)
                except PageNotAnInteger:
                    page_obj = paginator.page(1)
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)
                return Response({'result':{'status':'Created','data':list(page_obj)}})

            except IntegrityError as e:
                error_message = e.args
                return Response({
                'error':{'message':'DB error!',
                'detail':error_message,
                'status_code':status.HTTP_400_BAD_REQUEST,
                }},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user_create = CustomUser.objects.filetr(user_id=user,).update(

                                                role_id=role,
                                                city_id=city,
                                                first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                company_name=company_name,
                                                mobile_number=mobile_number,
                                                alternate_number=alternate_number,
                                                zip_code=zip_code,
                                                address=address,
                                                adhar_card=adhar_card,
                                                )

                posts = CustomUser.objects.all().values()
                paginator = Paginator(posts,10)
                try:
                    page_obj = paginator.get_page(selected_page_no)
                except PageNotAnInteger:
                    page_obj = paginator.page(1)
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)
                return Response({'result':{'status':'Created','data':list(page_obj)}})

            except IntegrityError as e:
                error_message = e.args
                return Response({
                'error':{'message':'DB error!',
                'detail':error_message,
                'status_code':status.HTTP_400_BAD_REQUEST,
                }},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})


        all_values = CustomUser.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})

# @method_decorator([AutorizationRequired], name='dispatch')
class PaymentDetailView(APIView):
    def get(self,request):
        CheckAccess(request)
        id = request.query_params.get('id')
        if id:
            owner_data = PaymentDetails.objects.filter(id=id).values()
            releated_drivers = Driver.objects.filter(owner_id=id).values()
            # print(owner_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

            if not owner_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':owner_data,'releated_drivers':releated_drivers}})

        else:
            owner_data = PaymentDetails.objects.all().values()
            return Response({'result':{'status':'GET','data':owner_data}})

    def post(self,request):
        CheckAccess(request)
        data = request.data

        in_order_id =data.get('in_order_id')
        amount=data.get('amount')
        provider=data.get('provider')
        pay_status=data.get('pay_status_id')

        selected_page_no =1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)

        try:
            payment_details = PaymentDetails.objects.create(
                                            in_order_id=in_order_id,
                                            amount=amount,
                                            provider=provider,
                                            pay_status_id=pay_status,
                                            )
            posts = PaymentDetails.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        in_order_id =data.get('in_order_id')
        amount=data.get('amount')
        provider=data.get('provider')
        pay_status=data.get('pay_status_id')

        try:
            emp_role= PaymentDetails.objects.filter(id=pk).update(
                                            in_order_id=in_order_id,
                                            amount=amount,
                                            provider=provider,
                                            pay_status_id=pay_status,
                                            )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})
        all_values = PaymentDetails.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})

# @method_decorator([AutorizationRequired], name='dispatch')
class DriverView(APIView):
    def get(self,request):
        # CheckAccess(request)
        id = request.query_params.get('id')
        response={}
        if id:
            try:
                driver_data = Driver.objects.filter(id=id).values('id','vehicle_id','vehicle__vehicle_status','vehicle__id','user_id','owner_id','driver_driving_license','badge','user__role__id','user__first_name','user__mobile_number','passbook_img','vehicle__vehicle_name','vehicle__vehicle_number','vehicle__permit_front_side_img_path','insurence_img','vehicle__pollution_certificate_front_side_img_path','vehicle__registration_certificate_back_side_img_path','vehicle__registration_certificate_front_side_img_path','license_img_back','user__adhar_card_front_side_img_path','user__adhar_card_back_side_img_path','license_img_front','vehicle__vehicletypes__vehicle_type_name', 'license_expire_date', 'insurence_expire_date', 'fitness_certificate_expire_date', 'vehicle__permit_expire_date', 'vehicle__rc_expire_date', 'vehicle__emission_test_expire_date', 'is_online', 'is_active', 'driver_status')

                # owner_data = Owner.objects.filter(id=driver_data.owner_id).values()
                # driver_details = {
                #                                 'user_id':driver_data.user_id,
                #                                 'role_id':driver_data.role_id,
                #                                 'city_id':driver_data.city_id,
                #                                 'owner':driver_data.owner,
                #                                 'driver_name':driver_data.driver_name,
                #                                 'driver_phone_number':driver_data.driver_phone_number,
                #                                 'driver_driving_license':driver_data.driver_driving_license,
                #                                 'badge':driver_data.badge,
                #                                 'aadhaar_card':driver_data.aadhaar_card,
                                            

                # }
                return Response({'result':{'status':'GET by Id','driver_data':driver_data}})
            except Driver.DoesNotExist as e:
                error_message = e.args
                return Response({
                'error':{'message':'Driver not exists error!',
                'detail':error_message,
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
            except IntegrityError as e:
                error_message = e.args
                return Response({
                'error':{'message':'DB error!',
                'detail':error_message,
                'status_code':status.HTTP_400_BAD_REQUEST,
                }},status=status.HTTP_400_BAD_REQUEST)
        else:
            driver_data = Driver.objects.all().values('id','vehicle_id','vehicle__vehicle_status','user_id','owner_id','driver_driving_license','badge','user_id','user__role__id','user__first_name','user__mobile_number','passbook_img','vehicle__vehicle_name','vehicle__vehicle_number','vehicle__permit_front_side_img_path','vehicle__pollution_certificate_front_side_img_path','vehicle__registration_certificate_back_side_img_path','vehicle__registration_certificate_front_side_img_path','license_img_back','vehicle__vehicletypes__vehicle_type_name', 'license_expire_date', 'insurence_expire_date', 'fitness_certificate_expire_date', 'vehicle__permit_expire_date', 'vehicle__rc_expire_date', 'vehicle__emission_test_expire_date', 'is_online', 'is_active', 'driver_status')
            return Response({'result':{'status':'GET','data':driver_data}})

        # if id:
        #     driver_datas = Driver.objects.filter(id=id)
        #     if driver_datas:
        #         driver_data = Driver.objects.get(id=id)
        #
        #         # owner_data = Owner.objects.filter(id=driver_data.owner_id).values()
        #         driver_details = {
        #                                         'user_id':driver_data.user_id,
        #                                         # 'role_id':driver_data.role_id,
        #                                         # 'city_id':driver_data.city_id,
        #                                         'owner':driver_data.owner,
        #                                         # 'driver_name':driver_data.driver_name,
        #                                         # 'driver_phone_number':driver_data.driver_phone_number,
        #                                         'driver_driving_license':driver_data.driver_driving_license,
        #                                         'badge':driver_data.badge,
        #                                         # 'aadhaar_card':driver_data.aadhaar_card,
        #
        #
        #         }
        #
        #
        #         print(driver_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')
        #
        #         if not driver_data:
        #             return Response({
        #             'error':{'message':'Record not found!',
        #             'status_code':status.HTTP_404_NOT_FOUND,
        #             }},status=status.HTTP_404_NOT_FOUND)
        #
        #         return Response({'result':{'status':'GET by Id','driver_details':driver_details}})
        #     else:
        #         header_response = {}
        #         response['error'] = {'error': {
        #                 'detail': 'Record not found!', 'status': status.HTTP_401_UNAUTHORIZED}}
        #         return Response(response['error'], status=status.HTTP_400_BAD_REQUEST)
        #
        #
        # else:
        #     driver_data = Driver.objects.all().values()
        #     return Response({'result':{'status':'GET','data':driver_data}})

    def post(self,request):
        CheckAccess(request)
        data = request.data

        driver_driving_license=data.get('driver_driving_license')
        badge=data.get('badge')
        user_id=data.get('user_id')
        vehicle_id=data.get('vehicle_id')
        owner=data.get('owner_id') # string If Owner is a driver, then owner_ID is -1
        license_status=data.get('license_status')
        subcription=data.get('subcription_id')
        # driver_status=data.get('driver_status')

        get_month = Subscription.objects.get(id=subcription)
        vsd = datetime.now()
        ved = pd.to_datetime(str(vsd)) + pd.DateOffset(months=int(get_month.validity_period))
        start1 = str(vsd).split(" ")[0]
        end1 = str(ved).split(" ")[0]
        # print(start1,'start1 split time')
        # print(end1,'end1 split time')
        validity_start_date = time.mktime(datetime.strptime(str(start1), "%Y-%m-%d").timetuple())
        # print(validity_start_date,'validity_start_date timestamp')
        validity_end_date = time.mktime(datetime.strptime(str(end1), "%Y-%m-%d").timetuple())
        # print(validity_end_date,'validity_end_date timestamp')



        user_details = User.objects.get(id=user_id)


        user_name = str(user_details.first_name)+str(random.randint(0,1000))

        driving_license_image=data.get('driving_license_image')
        license_img=data.get('license_img')
        permit_img=data.get('permit_img')
        fitness_certificate_img=data.get('fitness_certificate_img')
        emission_test_img=data.get('emission_test_img')
        insurence_img=data.get('insurence_img')
        rc_img=data.get('rc_img')
        passbook_img=data.get('passbook_img')


        selected_page_no =1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)


        try:
            driver_data = Driver.objects.create(
                driver_driving_license = driver_driving_license,
                badge = badge,
                user_id = user_id,
                vehicle_id = vehicle_id,
                owner = owner,
                base64=driving_license_image,
                subcription_id=subcription,
                license_status=license_status,
                validity_start_date=validity_start_date,
                validity_end_date=validity_end_date,
            )

            if driver_data.driver_status == "validate":
                driver_data.driver_status = "waiting for verification"
                driver_data.save()

            driver_details ={
                'driver_driving_license': driver_data.driver_driving_license,
                'badge': driver_data.badge,
                'user_id': driver_data.user_id,
                'vehicle_id': driver_data.vehicle_id,
                'owner': driver_data.owner,
                'driver_status':driver_data.driver_status,
            }

            if driving_license_image:
                split_base_url_data=driving_license_image.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = driving_license_image.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/driving_license/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.driving_license_image_path = 'http://127.0.0.1:8000/media/driving_license/'+ (str(image_name))
                driver_data.save()
            if license_img:
                split_base_url_data=license_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = license_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/license_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.license_img = 'http://127.0.0.1:8000/media/license_img/'+ (str(image_name))
                driver_data.save()
            if permit_img:
                split_base_url_data=permit_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = permit_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/permit_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.permit_img = 'http://127.0.0.1:8000/media/permit_img/'+ (str(image_name))
                driver_data.save()

            if fitness_certificate_img:
                split_base_url_data=fitness_certificate_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = fitness_certificate_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/fitness_certificate_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.fitness_certificate_img = 'http://127.0.0.1:8000/media/fitness_certificate_img/'+ (str(image_name))
                driver_data.save()

            if emission_test_img:
                split_base_url_data=emission_test_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = emission_test_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/emission_test_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.emission_test_img = 'http://127.0.0.1:8000/media/emission_test_img/'+ (str(image_name))
                driver_data.save()

            if insurence_img:
                split_base_url_data=insurence_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = insurence_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/insurence_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.insurence_img = 'http://127.0.0.1:8000/media/insurence_img/'+ (str(image_name))
                driver_data.save()

            if rc_img:
                split_base_url_data=rc_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = rc_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/rc_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.rc_img = 'http://127.0.0.1:8000/media/rc_img/'+ (str(image_name))
                driver_data.save()

            if passbook_img:
                split_base_url_data=passbook_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = passbook_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/passbook_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.passbook_img = 'http://127.0.0.1:8000/media/passbook_img/'+ (str(image_name))
                driver_data.save()

            posts = Driver.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created',"created_driver_data":driver_details,'all_driver_data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        driver_driving_license=data.get('driver_driving_license')
        badge=data.get('badge')
        user_id=data.get('user_id')
        vehicle_id=data.get('vehicle_id')
        driver_status=data.get('driver_status')
        owner=data.get('owner') # string
        license_status=data.get('license_status')


        subcription=data.get('subcription_id')

        get_month = Subscription.objects.get(id=subcription)
        vsd = datetime.now()
        ved = pd.to_datetime(str(vsd)) + pd.DateOffset(months=int(get_month.validity_period))
        start1 = str(vsd).split(" ")[0]
        end1 = str(ved).split(" ")[0]
        # print(start1,'start1 split time')
        # print(end1,'end1 split time')
        validity_start_date = time.mktime(datetime.strptime(str(start1), "%Y-%m-%d").timetuple())
        # print(validity_start_date,'validity_start_date timestamp')
        validity_end_date = time.mktime(datetime.strptime(str(end1), "%Y-%m-%d").timetuple())
        # print(validity_end_date,'validity_end_date timestamp')


        user_details = User.objects.get(id=user_id)


        user_name = str(user_details.first_name)+str(random.randint(0,1000))

        # base64=data.get('base64')
        #
        #
        #
        # driving_license_image=data.get('driving_license_image')
        #
        # split_base_url_data=driving_license_image.split(';base64,')[1]
        # imgdata1 = base64.b64decode(split_base_url_data)
        #
        # data_split = driving_license_image.split(';base64,')[0]
        # extension_data = re.split(':|;', data_split)[1]
        # guess_extension_data = guess_extension(extension_data)
        #
        # # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
        # filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/driving_license/"+user_name+guess_extension_data
        # image_name = user_name+guess_extension_data
        # ss=  open(filename1, 'wb')
        # print(ss)
        # ss.write(imgdata1)
        # ss.close()

        try:
            Driver.objects.filter(id=pk).update(

                driver_driving_license = driver_driving_license,
                badge = badge,
                user_id = user_id,
                vehicle_id = vehicle_id,
                owner = owner,
                base64=driving_license_image,
                subcription_id=subcription,
                validity_start_date = validity_start_date,
                validity_end_date = validity_end_date,
                license_status=license_status,
                driver_status="waiting for verification",


            )
            driver_data = Driver.objects.get(id=pk)
            if driving_license_image:
                split_base_url_data=driving_license_image.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = driving_license_image.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/driving_license/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.driving_license_image_path = 'http://127.0.0.1:8000/media/driving_license/'+ (str(image_name))
                driver_data.save()
            if license_img:
                split_base_url_data=license_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = license_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/license_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.license_img = 'http://127.0.0.1:8000/media/license_img/'+ (str(image_name))
                driver_data.save()
            if permit_img:
                split_base_url_data=permit_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = permit_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/permit_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.permit_img = 'http://127.0.0.1:8000/media/permit_img/'+ (str(image_name))
                driver_data.save()

            if fitness_certificate_img:
                split_base_url_data=fitness_certificate_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = fitness_certificate_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/fitness_certificate_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.fitness_certificate_img = 'http://127.0.0.1:8000/media/fitness_certificate_img/'+ (str(image_name))
                driver_data.save()

            if emission_test_img:
                split_base_url_data=emission_test_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = emission_test_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/emission_test_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.emission_test_img = 'http://127.0.0.1:8000/media/emission_test_img/'+ (str(image_name))
                driver_data.save()

            if insurence_img:
                split_base_url_data=insurence_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = insurence_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/insurence_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.insurence_img = 'http://127.0.0.1:8000/media/insurence_img/'+ (str(image_name))
                driver_data.save()

            if rc_img:
                split_base_url_data=rc_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = rc_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/rc_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.rc_img = 'http://127.0.0.1:8000/media/rc_img/'+ (str(image_name))
                driver_data.save()

            if passbook_img:
                split_base_url_data=passbook_img.split(';base64,')[1]
                imgdata1 = base64.b64decode(split_base_url_data)
                data_split = passbook_img.split(';base64,')[0]
                extension_data = re.split(':|;', data_split)[1]
                guess_extension_data = guess_extension(extension_data)
                # filename1 = "/eztime/site/public/media/driving_license_file/"+user_name+guess_extension_data
                filename1 = "/Users/apple/Documents/Ekfrazo/Django/logistics/Logistics/Logistics/media/passbook_img/"+user_name+guess_extension_data
                image_name = user_name+guess_extension_data
                ss=  open(filename1, 'wb')
                # print(ss)
                ss.write(imgdata1)
                ss.close()

                # course_data.thumbnail_link = 'https://logistics.thestorywallcafe.com/media/file_attachment/'+ (str(course_data.thumbnail)).split('thumbnail/')[1]
                driver_data.passbook_img = 'http://127.0.0.1:8000/media/passbook_img/'+ (str(image_name))
                driver_data.save()

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})


        all_values = Driver.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})

# @method_decorator([AutorizationRequired], name='dispatch')
class ReviewApiView(APIView):
    def get(self,request):
        data=request.data
        # CheckAccess(request)
        id = request.query_params.get('id')
        if id:
            all_data = Review.objects.filter(id=id).values()
            # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})

        else:
            all_data = Review.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        CheckAccess(request)
        data = request.data
        # print('data',data)
        review_stars=data.get('review_stars')
        comment=data.get('comment')
        review_type=data.get('review_type')
        linked_id=data.get('linked_id')

        selected_page_no =1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)

        try:
            emp_role = Review.objects.create(
                                            review_stars=review_stars,
                                            comment=comment,
                                            review_type=review_type,
                                            linked_id=linked_id
                                        )

            posts = Review.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        data = request.data
        review_stars=data.get('review_stars')
        comment=data.get('comment')
        review_type=data.get('review_type')
        linked_id=data.get('linked_id')

        try:
            emp_role= Review.objects.filter(id=pk).update(review_stars=review_stars,
                                                            comment=comment,
                                                            review_type=review_type,
                                                            linked_id=linked_id
                                        )



        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code":"AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})

        all_values = Review.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})

# @method_decorator([AutorizationRequired], name='dispatch')
class CustomerAddressView(APIView):
    def get(self,request):
        data=request.data
        # CheckAccess(request)
        id = request.query_params.get('id')
        if id:
            all_data = CustomerAddress.objects.filter(id=id).values()
            # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})


        else:
            all_data = CustomerAddress.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        CheckAccess(request)
        data = request.data
        user=data.get('user_id')
        city=data.get('city_id')
        label=data.get('label')
        house_number=data.get('house_number')
        address=data.get('address')
        area=data.get('area')
        landmark=data.get('landmark')
        zipcode=data.get('zipcode')
        latitude=data.get('latitude')
        longitude=data.get('longitude')
        contact_number=data.get('contact_number')
        contact_name=data.get('contact_name')

        selected_page_no =1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)

        try:
            emp_role = CustomerAddress.objects.create(
                                            user_id=user,
                                            city_id=city,
                                            label=label,
                                            house_number=house_number,
                                            address=address,
                                            area=area,
                                            landmark=landmark,
                                            zipcode=zipcode,
                                            latitude=latitude,
                                            longitude=longitude,
                                            contact_number=contact_number,
                                            contact_name=contact_name,
                                        )

            posts = CustomerAddress.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        user=data.get('user_id')
        city=data.get('city_id')
        label=data.get('label')
        house_number=data.get('house_number')
        address=data.get('address')
        area=data.get('area')
        landmark=data.get('landmark')
        zipcode=data.get('zipcode')
        latitude=data.get('latitude')
        longitude=data.get('longitude')
        contact_number=data.get('contact_number')
        contact_name=data.get('contact_name')

        try:
            emp_role= CustomerAddress.objects.filter(id=pk).update(user_id=user,
                                            city_id=city,
                                            label=label,
                                            house_number=house_number,
                                            address=address,
                                            area=area,
                                            landmark=landmark,
                                            zipcode=zipcode,
                                            latitude=latitude,
                                            longitude=longitude,
                                            contact_number=contact_number,
                                            contact_name=contact_name,
                                        )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})
        all_values = CustomerAddress.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})

# @method_decorator([AutorizationRequired], name='dispatch')
class PickupDetailsView(APIView):
    def get(self,request):
        CheckAccess(request)
        id = request.query_params.get('id')
        if id:
            all_data = PickupDetails.objects.filter(id=id).values()
            # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})


        else:
            all_data = PickupDetails.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        CheckAccess(request)
        data = request.data
        customer_address_id = data.get('customer_address_id')
        pd = data.get('pickup_date_time')

        pickup_date_time = time.mktime(datetime.datetime.strptime(pd, "%d/%m/%Y %I:%M %p").timetuple())

        selected_page_no =1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)


        try:
            emp_role = PickupDetails.objects.create(
                                            customer_address_id=customer_address_id,
                                            pickup_date_time = pickup_date_time,
                                        )


            posts = PickupDetails.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        customer_address_id = data.get('customer_address_id')
        pd = data.get('pickup_date_time')
        pt = data.get('pickup_time')

        pickup_date_time = time.mktime(datetime.datetime.strptime(pd, "%d/%m/%Y %I:%M %p").timetuple())
        try:
            emp_role= PickupDetails.objects.filter(id=pk).update(
                                            customer_address_id=customer_address_id,
                                            pickup_date_time = pickup_date_time,
                                        )



        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})
        all_values = PickupDetails.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})

# @method_decorator([AutorizationRequired], name='dispatch')
class DropDetailsView(APIView):
    def get(self,request):
        CheckAccess(request)
        id = request.query_params.get('id')
        if id:
            all_data = DropDetails.objects.filter(id=id).values()
            # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})

        else:
            all_data = DropDetails.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        CheckAccess(request)
        data = request.data
        customer_address_id=data.get('customer_address_id')
        priority=data.get('priority')
        ddt = data.get('drop_date_time')

        drop_date_time = time.mktime(datetime.strptime(ddt, "%d/%m/%Y %I:%M %p").timetuple())


        selected_page_no =1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)

        try:
            emp_role = DropDetails.objects.create(
                                            customer_address_id=customer_address_id,
                                            priority=priority,
                                            drop_date_time=drop_date_time,
                                        )

            posts = DropDetails.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        customer_address_id=data.get('customer_address_id')
        priority=data.get('priority')
        ddt = data.get('drop_date_time')

        drop_date_time = time.mktime(datetime.datetime.strptime(ddt, "%d/%m/%Y %I:%M %p").timetuple())


        try:
            emp_role= DropDetails.objects.filter(id=pk).update(customer_address_id=customer_address_id,
                                            priority=priority,
                                            drop_date_time=drop_date_time,
                                        )



        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})


        all_values = DropDetails.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})


# @method_decorator([AutorizationRequired], name='dispatch')
class PlacedOrderView(APIView):
    def get(self,request):
        CheckAccess(request)
        user_id = request.query_params.get('user_id')
        role_id = request.query_params.get('role_id')
        id = request.query_params.get('id')
       
        try:
            get_sub_id = Driver.objects.get(user_id=user_id)
        except Driver.DoesNotExist as e:
            error_message = e.args
            return Response({
            'error':{'message':'Driver not exists error!',
            'detail':error_message,
            'status_code':status.HTTP_404_NOT_FOUND,
            }},status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

        now_date_date = datetime.now()
        now_date = str(now_date_date).split(" ")[0]
        now = time.mktime(datetime.strptime(str(now_date), "%Y-%m-%d").timetuple())

        if id:
            if (get_sub_id.validity_end_date <= now & get_sub_id.license_status == '1' ):
                all_data = PlacedOrder.objects.filter(id=id).values()
                # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

                if not all_data:
                    return Response({
                    'error':{'message':'Record not found!',
                    'status_code':status.HTTP_404_NOT_FOUND,
                    }},status=status.HTTP_404_NOT_FOUND)

                return Response({'result':{'status':'GET by Id','data':all_data}})
            else:
                return Response({
                    'error':{'message':'You are not authorized to get the orders, Please contact admin!',
                    'status_code':status.HTTP_401_UNAUTHORIZED,
                    }},status=status.HTTP_401_UNAUTHORIZED)
        else:
            if (float(get_sub_id.validity_end_date) >= float(now) and get_sub_id.license_status == '1'):
                all_data = PlacedOrder.objects.all().values()
                return Response({'result':{'status':'GET','data':all_data}})
            else:
                return Response({
                    'error':{'message':'You are not authorized to get the orders, Please contact admin!',
                    'status_code':status.HTTP_401_UNAUTHORIZED,
                    }},status=status.HTTP_401_UNAUTHORIZED)

    def post(self,request):
        CheckAccess(request)
        data = request.data
        # print(data,'dataaaaaaaaaaaa')
        user=data['user_id']
        pickup_id=data['pickup_id']
        drop_id_list=data['drop_id_list']#only 3
        vehicle_type_id=data['vehicle_type_id']
        # print(data,'dataaaa')
        response = {}
        # time.mktime(datetime.datetime.strptime(pd, "%d/%m/%Y %I:%M %p").timetuple())
        if len(drop_id_list)>3:
            header_response = {}
            response['error'] = {'error': {
                    'detail': 'you can select only 3 stops', 'status': status.HTTP_401_UNAUTHORIZED}}
            return Response(response['error'], status=status.HTTP_400_BAD_REQUEST)
        else:

            drop_list = []

            for i in pickup_id:
                try:
                    # print(i,'city')
                    pickup_address = CustomerAddress.objects.create(
                                                    user_id=user,
                                                    city_id=int(i['city_id']),
                                                    label=i['label'],
                                                    house_number=i['house_number'],
                                                    address=i['address'],
                                                    area=i['area'],
                                                    landmark=i['landmark'],
                                                    zipcode=i['zipcode'],
                                                    latitude=i['latitude'],
                                                    longitude=i['longitude'],
                                                    contact_number=i['contact_number'],
                                                    contact_name=i['contact_name'],
                                                )


                except IntegrityError as e:
                    error_message = e.args
                    return Response({
                    'error':{'message':'DB error!',
                    'detail':error_message,
                    'status_code':status.HTTP_400_BAD_REQUEST,
                    }},status=status.HTTP_400_BAD_REQUEST)

                try:
                    pickup_date = time.mktime(datetime.strptime(i['pickup_date'], "%d/%m/%Y").timetuple())
                    pickup_detail = PickupDetails.objects.create(
                                                    customer_address_id=pickup_address.id,
                                                    pickup_date = pickup_date,
                                                    pickup_time = i['pickup_time']
                                                )

                except IntegrityError as e:
                    error_message = e.args
                    return Response({
                    'error':{'message':'DB error!',
                    'detail':error_message,
                    'status_code':status.HTTP_400_BAD_REQUEST,
                    }},status=status.HTTP_400_BAD_REQUEST)


            for j in drop_id_list:
                try:
                    drop_address = CustomerAddress.objects.create(
                                                    user_id=user,
                                                    city_id=j['city_id'],
                                                    label=j['label'],
                                                    house_number=j['house_number'],
                                                    address=j['address'],
                                                    area=j['area'],
                                                    landmark=j['landmark'],
                                                    zipcode=j['zipcode'],
                                                    latitude=j['latitude'],
                                                    longitude=j['longitude'],
                                                    contact_number=j['contact_number'],
                                                    contact_name=j['contact_name'],
                                                )

                except IntegrityError as e:
                    error_message = e.args
                    return Response({
                    'error':{'message':'DB error!',
                    'detail':error_message,
                    'status_code':status.HTTP_400_BAD_REQUEST,
                    }},status=status.HTTP_400_BAD_REQUEST)

                try:
                    drop_date = time.mktime(datetime.strptime(j['drop_date'], "%d/%m/%Y").timetuple())

                    drop_details = DropDetails.objects.create(
                                                    customer_address_id=drop_address.id,
                                                    priority=j['priority'],
                                                    drop_date =drop_date,
                                                    drop_time = j['drop_time']
                                                )
                    drop_list.append(drop_details.id)
                except IntegrityError as e:
                    error_message = e.args
                    return Response({
                    'error':{'message':'DB error!',
                    'detail':error_message,
                    'status_code':status.HTTP_400_BAD_REQUEST,
                    }},status=status.HTTP_400_BAD_REQUEST)
            try:
                get_price_km = VehicleTypes.objects.get(id=vehicle_type_id )
                est_km = 100
                est_cost = est_km * int(get_price_km.per_km_price)
                client_order = PlacedOrder.objects.create(
                                                user_id=user,
                                                pickup_id=pickup_detail.id,
                                                vehicle_type_id=vehicle_type_id,
                                                drop=drop_list,
                                                estimated_kms=est_km,
                                                estimated_amount=est_cost,
                                            )


                place_order = PlacedOrder.objects.all().values()

                return Response({'result':{'status':'Created','place_order':place_order}})

            except IntegrityError as e:
                    error_message = e.args
                    return Response({
                    'error':{'message':'DB error!',
                    'detail':error_message,
                    'status_code':status.HTTP_400_BAD_REQUEST,
                    }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        user=data.get('user_id')
        pickup=data.get('pickup_id')
        drop=data.get('drop')
        estimated_kms=data.get('estimated_kms')
        estimated_amount=data.get('estimated_amount')

        try:
            emp_role= PlacedOrder.objects.filter(id=pk).update(user_id=user,
                                            pickup_id=pickup,
                                            drop=drop,
                                            estimated_kms=estimated_kms,
                                            estimated_amount=estimated_amount,)

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})


        all_values = PlacedOrder.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})

# @method_decorator([AutorizationRequired], name='dispatch')
class CouponsView(APIView):
    def get(self,request):
        data=request.data
        user_role_name=data.get('user_role_name')
        # CheckAccess(request)
        id = request.query_params.get('id')
        if id:
            all_data = Coupons.objects.filter(id=id).values()
            # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})


        else:
            all_data = Coupons.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        coupon_name=data.get('coupon_name')
        coupon_discount=data.get('coupon_discount')


        selected_page_no =1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)


        try:
            emp_role = Coupons.objects.create(
                                            coupon_name=coupon_name,
                                            coupon_discount=coupon_discount,
                                        )


            posts = Coupons.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)


        data = request.data
        coupon_name=data.get('coupon_name')
        coupon_discount=data.get('coupon_discount')

        try:
            emp_role= Coupons.objects.filter(id=pk).update(coupon_name=coupon_name,
                                            coupon_discount=coupon_discount,)



        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})


        all_values = Coupons.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})



# @method_decorator([AutorizationRequired], name='dispatch')
class InOrderView(APIView):
    def get(self,request):
        CheckAccess(request)
        id = request.query_params.get('id')
        if id:
            all_data = InOrder.objects.filter(id=id).values()
            # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})


        else:
            all_data = InOrder.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        CheckAccess(request)
        data = request.data
        placed_order=data.get('placed_order_id')
        coupon=data.get('coupon_id')
        driver=data.get('driver_id')
        status_detail=data.get('status_details_id')
        final_amount=data.get('final_amount')
        comment=data.get('comment')

        selected_page_no =1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)

        try:
            emp_role = InOrder.objects.create(placed_order_id=placed_order,
                                                coupon_id=coupon,
                                                driver_id=driver,
                                                status_details_id=status_detail,
                                                final_amount=final_amount,
                                                comment=comment,

                                        )

            posts = InOrder.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        placed_order=data.get('placed_order_id')
        coupon=data.get('coupon_id')
        driver=data.get('driver_id')
        status_detail=data.get('status_details_id')
        final_amount=data.get('final_amount')
        comment=data.get('comment')

        try:
            emp_role= InOrder.objects.filter(id=pk).update(placed_order_id=placed_order,
                                                coupon_id=coupon,
                                                driver_id=driver,
                                                status_details_id=status_detail,
                                                final_amount=final_amount,
                                                comment=comment,

                                            )

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})


        all_values = InOrder.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})


#-----------------------------------------------dMaster ------------------------------------------------------------------------------
# @method_decorator([AutorizationRequired], name='dispatch')

class SubscriptionView(APIView):
    def get(self,request):
        # CheckAccess(request)
        data=request.data
        user_role_name=data.get('user_role_name')
        
        id = request.query_params.get('id')
        if id:
            all_data = Subscription.objects.filter(id=id).values()
            # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})


        else:
            all_data = Subscription.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        # CheckAccess(request)
        data = request.data
        user_role_name=data.get('user_role_name')
        sub_plan_name=data.get('sub_plan_name')
        price=data.get('price')
        validity_period=data.get('validity_period')

        selected_page_no =1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)
        try:
            emp_role = Subscription.objects.create(sub_plan_name=sub_plan_name,
                                                    price=price,
                                                    validity_period=validity_period,

                                        )

            posts = Subscription.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        sub_plan_name=data.get('sub_plan_name')
        price=data.get('price')
        validity_period=data.get('validity_period')

        try:
            emp_role= Subscription.objects.filter(id=pk).update(sub_plan_name=sub_plan_name,
                                                    price=price,
                                                    validity_period=validity_period,

                                            )


        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})

        all_values = Subscription.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})

# @method_decorator([AutorizationRequired], name='dispatch')
class AccountView(APIView):
    def get(self,request):
        CheckAccess(request)

        id = request.query_params.get('id')
        if id:
            all_data = Account.objects.filter(id=id).values()
            # print(all_data,'AAAAAAAAAAAAAAAAAAAAAAAAAA')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})

        else:
            all_data = Account.objects.all().values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        CheckAccess(request)
        data = request.data
        user_id=data.get('user_id')
        acc_holder_name=data.get('acc_holder_name')
        bank=data.get('bank')
        branch=data.get('branch')
        account_no=data.get('account_no')
        ifsc_code=data.get('ifsc_code')

        selected_page_no =1
        page_number = request.GET.get('page')
        if page_number:
            selected_page_no = int(page_number)

        try:
            emp_role = Account.objects.create(user_id=user_id,
                                            acc_holder_name=acc_holder_name,
                                            bank=bank,branch=branch,
                                            account_no=account_no,
                                            ifsc_code=ifsc_code)

            posts = Account.objects.all().values()
            paginator = Paginator(posts,10)
            try:
                page_obj = paginator.get_page(selected_page_no)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            return Response({'result':{'status':'Created','data':list(page_obj)}})

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        user_id=data.get('user_id')
        acc_holder_name=data.get('acc_holder_name')
        bank=data.get('bank')
        branch=data.get('branch')
        account_no=data.get('account_no')
        ifsc_code=data.get('ifsc_code')

        try:
            emp_role= Account.objects.filter(id=pk).update(user_id=user_id,
                                            acc_holder_name=acc_holder_name,
                                            bank=bank,branch=branch,
                                            account_no=account_no,
                                            ifsc_code=ifsc_code)

        except IntegrityError as e:
            error_message = e.args
            return Response({
            'error':{'message':'DB error!',
            'detail':error_message,
            'status_code':status.HTTP_400_BAD_REQUEST,
            }},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'status':'Updated'}})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})


        all_values = Account.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})



class DriverLatitudeLongitudeView(APIView):
    def post(self,request):
        data = request.data
        driver_id = data.get('driver_id')
        live_lattitude = data.get('live_lattitude')
        live_longitude = data.get('live_longitude')

        driver_log_lat = Driver.objects.filter(id=driver_id).update(
            live_lattitude=live_lattitude,live_longitude=live_longitude
        )

        return Response({'result':{'status':'Driver Live Location Updated'}})

class UserDestinationsView(APIView):
    def post(self,request):
        data = request.data
        driver_reg_no = data.get('driver_reg_no')
        destination_array = data.get('destination_array')

        # print(destination_array,'destination_array')

        # driver_log_lat = Driver.objects.filter(id=driver_id).update(
        #     live_lattitude=live_lattitude,live_longitude=live_longitude
        # )

        return Response({'result':{'status':'Driver destination_array recieved'}})

# ---------------------------------------------------------------------------------------------------------------------------------------
import datetime
# datetime.datetime.utcnow()

class LoginApi(APIView):
    def post(self, request):
        data = request.data
        user_role_name=data['user_role_name']
        # otp = random.randint(100000, 999999)
        # request.session['otp'] = otp
        if CustomUser.objects.filter(Q(mobile_number=data['mobile_number']) & Q(role__user_role_name=data['user_role_name'])).exists():
            sendMobileOTp(data['mobile_number'])
            customUser = CustomUser.objects.get(mobile_number=data['mobile_number'], role__user_role_name=data['user_role_name'])

            auth_token = jwt.encode({'user_id': customUser.id}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

            if Driver.objects.filter(user_id=customUser.id).exists():
                driver_obj = Driver.objects.get(user_id=customUser.id)
                return Response({'message':'Login Successfull', 'otp': "otp", 'user_id': customUser.id, 'token': auth_token, 'vehicle_id': driver_obj.vehicle_id})

            return Response({'message':'Login Successfull', 'otp': "otp", 'user_id': customUser.id, 'token': auth_token})

            # send this otp to his/her mobile number
        # if CustomUser.objects.filter(Q(mobile_number=data['mobile_number']) & Q(role__user_role_name=data['user_role_name'])).exists():
        #     customUser = CustomUser.objects.get(mobile_number=data['mobile_number'])

        #     auth_token = jwt.encode({'user_id': customUser.id, 'exp': datetime.utcnow() + timedelta(days=5)}, str(settings.JWT_SECRET_KEY), algorithm="HS256")

        #     return Response({'message':'Login Successfull', 'otp': otp, 'user_id': customUser.id, 'token': auth_token})
        else:
            return Response({'message':'User Does not exists'},  status=status.HTTP_406_NOT_ACCEPTABLE)
            # pass

        

class UserLoginView(APIView):
    def post(self,request):
        data = request.data
        mobile_number = data.get('mobile_number')

        sendMobileOTp(mobile_number)
        # otp = random.randint(100000, 999999)
        # request.session['otp'] = otp
        if CustomUser.objects.filter(Q(mobile_number=mobile_number) & Q(role__user_role_name=data['user_role_name'])).exists():
            return Response({'driver already exist with this mobile number'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if CustomUser.objects.filter(Q(mobile_number=mobile_number) & Q(role__user_role_name=data['user_role_name'])).exists():
            return Response({'user already exist with this mobile number'}, status=status.HTTP_406_NOT_ACCEPTABLE)
 
        if data['user_role_name'] == None:
                return Response({'message': 'role name is required'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            if data['user_role_name'] == 'Driver':
                customUser = CustomUser.objects.create(mobile_number=mobile_number, role_id=3)
                driver_obj = Driver.objects.create(user_id=customUser.id, driver_status="Registered with Mobile Number")
            else:
                customUser = CustomUser.objects.create(mobile_number=mobile_number, role_id=2)
            
            return Response({"message": "user created successfully", 'otp': "otp", 'user_id': customUser.id})

class OtpVerificationApi(APIView):
    def post(self, request):
        data = request.data
        user_role = data.get('user_role')
        verified_otp = verifyOTP(data['moibile_number'], data['otp'])
        return Response(verified_otp)
        # if(request.session['otp'] == data['otp']):

        #     return Response({'message': "login successfull"})
        # else:
        #     return Response({'error': "otp does not matched"}, status=status.HTTP_406_NOT_ACCEPTABLE)






# def convertBase64(image, image_name, driver_id, folder_name):
#     split_base_url_data = image.split(';base64,')[1]
#     imgdata1 = base64.b64decode(split_base_url_data)
#     filename1 = "/logistics/site/public/media/"+str(folder_name)+"/"+str(user_id)+image_name+'.png'
#     fname1 = '/'+str(folder_name)+'/'+str(user_id)+image_name+'.png'
#     ss=open(filename1, 'wb')
#     ss.write(imgdata1)
#     ss.close()  

    # return fname1



class UserSignup(APIView):
    def get(self,request):
        data=request.data
        profile_image_path=data.get('profile_image_path')
        id = request.query_params.get('id')
        # converted_profile_image = convertBase64(profile_image_path, 'profile_image_path', user_id, "profile")
        if id:
            all_data = CustomUser.objects.filter(id=request.query_params['id']).values('id','first_name','last_name','company_name','email','whatsup_number','profile_image_path')

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
            return Response({'result':{'status':'GET by Id','data':all_data}})

        else:
            all_data = CustomUser.objects.all().values('id','first_name','last_name','company_name','email','whatsup_number','profile_image_path')
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        data = request.data
        
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        company_name=data.get('company_name')
        email=data.get('email')
        whatsup_number=data.get('whatsup_number')
        user_id =data.get('user_id')

        customUser = CustomUser.objects.filter(id=user_id).update(
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            email=email
        )

        if whatsup_number is not None:
            CustomUser.objects.filter(id=user_id).update(
                whatsup_number= whatsup_number
            )
            return Response({'Message': 'Customer registered successfully!!'})
        else:
            return Response({'Message':'Customer registration is failed'})

    def put(self,request,pk):
        data = request.data
        data = request.data
        
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        company_name=data.get('company_name')
        email=data.get('email')
        whatsup_number=data.get('whatsup_number')
        user_id =data.get('user_id')
        profile_image_path=data.get('profile_image_path')


        if CustomUser.objects.filter(id=pk).exists():
            if profile_image_path == "":
                CustomUser.objects.filter(id=pk).update(first_name=first_name, last_name=last_name, company_name=company_name, email=email, whatsup_number=whatsup_number)
            else:
                converted_profile_image = convertBase64(profile_image_path, 'profile_image_path', uuid.uuid4(), "profile")
                CustomUser.objects.filter(id=pk).update(first_name=first_name, last_name=last_name, company_name=company_name, email=email, whatsup_number=whatsup_number, profile_image_path=converted_profile_image)
            
            custom_user = CustomUser.objects.get(id=pk)
            response_data = {
                'message': 'CustomUser is updated',
                'profile_image_path': custom_user.profile_image_path,
            }
            return Response(response_data)
        else:
            return Response({'error':'CustomUser id is not found'}, status=status.HTTP_404_NOT_FOUND)

import uuid
def convertBase64(image, image_name, driver_id, folder_name):
    if image is None:
        return None

    split_base_url_data = image.split(';base64,')[1]
    imgdata1 = base64.b64decode(split_base_url_data)
    filename1 = "/logistics/site/public/media/" + str(folder_name) + "/" + str(driver_id) + image_name + '.png'
    fname1 = '/' + str(folder_name) + '/' + str(driver_id) + image_name + '.png'
    ss = open(filename1, 'wb')
    ss.write(imgdata1)
    ss.close()

    return fname1
# def convertBase64(image, image_name, driver_id, folder_name):
#     split_base_url_data = image.split(';base64,')[1]
#     imgdata1 = base64.b64decode(split_base_url_data)
#     filename1 = "/logistics/site/public/media/"+str(folder_name)+"/"+str(driver_id)+image_name+'.png'
#     fname1 = '/'+str(folder_name)+'/'+str(driver_id)+image_name+'.png'
#     ss= open(filename1, 'wb')
#     ss.write(imgdata1)
#     ss.close()  

#     return fname1

# @method_decorator([AutorizationRequired], name='dispatch')
class VehicleView(APIView):
    def get(self,request):
        # CheckAccess(request)
        id = request.query_params.get('id')
        if id:
            all_data = Vehicle.objects.filter(id=id).values()

            if not all_data:
                return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)

            return Response({'result':{'status':'GET by Id','data':all_data}})


        else:
            all_data = Vehicle.objects.filter(is_active=False).values()
            return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        data = request.data
        
        reg_certifiacte_front = data['reg_certifiacte_front']
        reg_certifiacte_back = data['reg_certifiacte_back']
        pollution_certifiactae_front = data['pollution_certifiactae_front']
        fitness_certifiacte_front = data['fitness_certifiacte_front']
        fitness_certifiacte_back = data['fitness_certifiacte_back']
        permit_image = data['permit_image']
        insurance_image = data['insurance_image']
        driver_id = data['driver_id']
        vehicle_status=data.get('vehicle_status')
        

        converted_reg_certificate_front = convertBase64(reg_certifiacte_front, 'driver',  uuid.uuid4(), "registration_certificate")
        converted_reg_certificate_back = convertBase64(reg_certifiacte_back, 'driver',  uuid.uuid4(), "registration_certificate")
        converted_pollution_certificate_front = convertBase64(pollution_certifiactae_front, 'driver',  uuid.uuid4(), "pollution_certificate")
        converted_fittness_certificate_front = convertBase64(fitness_certifiacte_front, 'driver',  uuid.uuid4(), "fitness_certificate")
        converted_fittness_certificate_back = convertBase64(fitness_certifiacte_back, 'driver',  uuid.uuid4(), "fitness_certificate")
        converted_permit_image = convertBase64(permit_image, 'driver',  uuid.uuid4(), "permit_front_side")
        converted_insurance_image = convertBase64(insurance_image, 'driver',  uuid.uuid4(), "permit_front_side")

        vehicle_obj = Vehicle.objects.create(
            vehicletypes_id=data['vehicle_type'],
            vehicle_name=data['vehicle_name'],
            vehicle_number = data['vehicle_number'],
            vehicle_status="waiting for verification",
            permit_front_side_img_path = converted_permit_image,
            registration_certificate_front_side_img_path = converted_reg_certificate_front,
            registration_certificate_back_side_img_path = converted_reg_certificate_back,
            pollution_certificate_front_side_img_path = converted_pollution_certificate_front
        )

        Driver.objects.filter(user_id=driver_id).update(
            insurence_img = converted_insurance_image,
            fitness_certificate_front_side_img_path = converted_fittness_certificate_front,
            fitness_certificate_back_side_img_path = converted_fittness_certificate_back,
            vehicle_id = vehicle_obj.id,
            driver_status = "waiting for verification"
            # vehicle_status="waiting for verification",
        )

        CustomUser.objects.filter(id=driver_id).update(
            vehicle_id = vehicle_obj.id
        )

        return Response({'message': 'vehicle details updated successfully', 'vehicle_id': vehicle_obj.id})

    def put(self,request):
        data = request.data
        
        reg_certifiacte_front = data['reg_certifiacte_front']
        reg_certifiacte_back = data['reg_certifiacte_back']
        pollution_certifiactae_front = data['pollution_certifiactae_front']
        fitness_certifiacte_front = data['fitness_certifiacte_front']
        fitness_certifiacte_back = data['fitness_certifiacte_back']
        permit_image = data['permit_image']
        insurance_image = data['insurance_image']
        driver_id = data['driver_id']
        vehicle_id = data['vehicle_id']
        # vehicle_status=data.get('vehicle_status')
        
         
        if Driver.objects.filter(Q(vehicle__vehicle_number=data['vehicle_number']) & ~Q(user_id=driver_id)).exists():
            return Response({'error': 'Vehicle number is already used by another driver'}, status=status.HTTP_400_BAD_REQUEST)

        else:

            if "data:image/" in reg_certifiacte_front:
                converted_reg_certificate_front = convertBase64(reg_certifiacte_front, 'driver', uuid.uuid4(), "registration_certificate")
                Vehicle.objects.filter(id=vehicle_id).update(registration_certificate_front_side_img_path = converted_reg_certificate_front)
            else:
                pass

            if "data:image/" in reg_certifiacte_back:
                converted_reg_certificate_back = convertBase64(reg_certifiacte_back, 'driver',  uuid.uuid4(), "registration_certificate")
                Vehicle.objects.filter(id=vehicle_id).update(registration_certificate_back_side_img_path = converted_reg_certificate_back)
            else:
                pass

            if "data:image/" in pollution_certifiactae_front:
                converted_pollution_certificate_front = convertBase64(pollution_certifiactae_front, 'driver',  uuid.uuid4(), "pollution_certificate")
                Vehicle.objects.filter(id=vehicle_id).update(pollution_certificate_front_side_img_path = converted_pollution_certificate_front)
            else:
                pass

            if "data:image/" in fitness_certifiacte_front:
                converted_fittness_certificate_front = convertBase64(fitness_certifiacte_front, 'driver',  uuid.uuid4(), "fitness_certificate")
                Driver.objects.filter(user_id=driver_id).update(fitness_certificate_front_side_img_path = converted_fittness_certificate_front)
            else:
                pass

            if "data:image/" in fitness_certifiacte_back:
                converted_fittness_certificate_back = convertBase64(fitness_certifiacte_back, 'driver',  uuid.uuid4(), "fitness_certificate")
                Driver.objects.filter(user_id=driver_id).update(fitness_certificate_back_side_img_path = converted_fittness_certificate_back)
            else:
                pass

            if "data:image/" in permit_image:
                converted_permit_image = convertBase64(permit_image, 'driver',  uuid.uuid4(), "permit_front_side")
                Vehicle.objects.filter(id=vehicle_id).update(permit_front_side_img_path = converted_permit_image)
            else:
                pass

            if "data:image/" in insurance_image:
                converted_insurance_image = convertBase64(insurance_image, 'driver',  uuid.uuid4(), "insurance_image")
                Driver.objects.filter(user_id=driver_id).update(insurence_img = converted_insurance_image)
            else:
                pass
            if 'vehicle_status' in request.data:
                if data.get('updated_by'):
                    vehicle_obj = Vehicle.objects.filter(id=vehicle_id).update(
                        vehicletypes_id=data['vehicle_type'],
                        vehicle_name=data['vehicle_name'],
                        vehicle_number=data['vehicle_number'],
                        is_active=data['vehicle_status'],
                        # permit_front_side_img_path = converted_permit_image,
                        # registration_certificate_front_side_img_path = converted_reg_certificate_front,
                        # registration_certificate_back_side_img_path = converted_reg_certificate_back,
                        # pollution_certificate_front_side_img_path = converted_pollution_certificate_front
                    )

                    Driver.objects.filter(vehicle_id=vehicle_id).update(
                        # insurence_img = converted_insurance_image,
                        # fitness_certificate_front_side_img_path = converted_fittness_certificate_front,
                        # fitness_certificate_back_side_img_path = converted_fittness_certificate_back,
                        # vehicle_id = vehicle_obj.id
                        is_active=data['vehicle_status'],
                    )
                else:
                    vehicle_obj = Vehicle.objects.filter(id=vehicle_id).update(
                        vehicletypes_id=data['vehicle_type'],
                        vehicle_name=data['vehicle_name'],
                        vehicle_number=data['vehicle_number'],
                        is_active=data['vehicle_status'],
                        vehicle_status="waiting for verification"
                        # permit_front_side_img_path = converted_permit_image,
                        # registration_certificate_front_side_img_path = converted_reg_certificate_front,
                        # registration_certificate_back_side_img_path = converted_reg_certificate_back,
                        # pollution_certificate_front_side_img_path = converted_pollution_certificate_front
                    )

                    Driver.objects.filter(vehicle_id=vehicle_id).update(
                        # insurence_img = converted_insurance_image,
                        # fitness_certificate_front_side_img_path = converted_fittness_certificate_front,
                        # fitness_certificate_back_side_img_path = converted_fittness_certificate_back,
                        # vehicle_id = vehicle_obj.id
                        is_active=data['vehicle_status'],
                        driver_status = "waiting for verification"
                    )
            else:
                if data.get('updated_by'):
                    vehicle_obj = Vehicle.objects.filter(id=vehicle_id).update(
                        vehicletypes_id=data['vehicle_type'],
                        vehicle_name=data['vehicle_name'],
                        vehicle_number=data['vehicle_number'],
                        # is_active=data['vehicle_status']
                        # vehicle_status="waiting for verification"
                        # permit_front_side_img_path = converted_permit_image,
                        # registration_certificate_front_side_img_path = converted_reg_certificate_front,
                        # registration_certificate_back_side_img_path = converted_reg_certificate_back,
                        # pollution_certificate_front_side_img_path = converted_pollution_certificate_front
                    )
                else:
                    vehicle_obj = Vehicle.objects.filter(id=vehicle_id).update(
                        vehicletypes_id=data['vehicle_type'],
                        vehicle_name=data['vehicle_name'],
                        vehicle_number=data['vehicle_number'],
                        # is_active=data['vehicle_status']
                        # vehicle_status="waiting for verification"
                        # permit_front_side_img_path = converted_permit_image,
                        # registration_certificate_front_side_img_path = converted_reg_certificate_front,
                        # registration_certificate_back_side_img_path = converted_reg_certificate_back,
                        # pollution_certificate_front_side_img_path = converted_pollution_certificate_front
                    )
                    Driver.objects.filter(vehicle_id=vehicle_id).update(driver_status = "waiting for verification")

            # Set vehicle status to "waiting for verification"
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle.vehicle_status = "waiting for verification"
            vehicle.save()

            # CustomUser.objects.filter(id=driver_id).update(
            #     vehicle_id = vehicle_obj.id
            # )

            return Response({'message': 'vehicle details updated successfully', 'vehicle_id': vehicle_id})

        # if 'vehicle_status' in request.data:
        #     vehicle_obj = Vehicle.objects.filter(id=vehicle_id).update(
        #         vehicletypes_id=data['vehicle_type'],
        #         vehicle_name=data['vehicle_name'],
        #         vehicle_number = data['vehicle_number'],
        #         is_active=data['vehicle_status']
        #         # vehicle_status="waiting for verification"
        #         # permit_front_side_img_path = converted_permit_image,
        #         # registration_certificate_front_side_img_path = converted_reg_certificate_front,
        #         # registration_certificate_back_side_img_path = converted_reg_certificate_back,
        #         # pollution_certificate_front_side_img_path = converted_pollution_certificate_front
        #     )

        #     Driver.objects.filter(vehicle_id=vehicle_id).update(
        #         # insurence_img = converted_insurance_image,
        #         # fitness_certificate_front_side_img_path = converted_fittness_certificate_front,
        #         # fitness_certificate_back_side_img_path = converted_fittness_certificate_back,
        #         # vehicle_id = vehicle_obj.id
        #         is_active = data['vehicle_status']
        #     )
        
        # vehicle_obj = Vehicle.objects.filter(id=vehicle_id).update(
        #     vehicletypes_id=data['vehicle_type'],
        #     vehicle_name=data['vehicle_name'],
        #     vehicle_number = data['vehicle_number'],
        #     # is_active=data['vehicle_status']
        #     # vehicle_status="waiting for verification"
        #     # permit_front_side_img_path = converted_permit_image,
        #     # registration_certificate_front_side_img_path = converted_reg_certificate_front,
        #     # registration_certificate_back_side_img_path = converted_reg_certificate_back,
        #     # pollution_certificate_front_side_img_path = converted_pollution_certificate_front
        # )

        # # CustomUser.objects.filter(id=driver_id).update(
        # #     vehicle_id = vehicle_obj.id
        # # )

        # return Response({'message': 'vehicle details updated successfully', 'vehicle_id': vehicle_id})

    def delete(self,request,pk):
        # return_data = CheckAccess(request)
        # print(return_data,'return auth')
        # if return_data != 1:
        #     return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You not authories to perform this operation'}}, status=status.HTTP_401_UNAUTHORIZED)

        test = (0,{})


        all_values = Vehicle.objects.filter(id=pk).delete()
        if test == all_values:

            return Response({
                'error':{'message':'Record not found!',
                'status_code':status.HTTP_404_NOT_FOUND,
                }},status=status.HTTP_404_NOT_FOUND)
        else:
            # all_values = EmployeeDetail.objects.filter(id=pk).delete()
            return Response({'result':{'status':'deleted'}})

from django.db.models import F

class DriverSignup(APIView):
    def get(self, request):
        if request.query_params:
            driver_obj = Driver.objects.filter(user_id=request.query_params['user_id']).values('id','vehicle_id','vehicle__vehicle_status','vehicle__vehicle_name', 'vehicle__vehicle_number', 'driver_driving_license', 'user__first_name', 'badge', 'user__adhar_card_front_side_img_path', 'user__adhar_card_back_side_img_path', 'user__role__user_role_name', 'user__mobile_number', 'vehicle__permit_front_side_img_path', 'vehicle__registration_certificate_front_side_img_path', 'vehicle__registration_certificate_back_side_img_path', 'vehicle__pollution_certificate_front_side_img_path', 'license_img_front', 'license_img_back', 'insurence_img', 'passbook_img', 'user_id', 'owner_id', 'fitness_certificate_back_side_img_path','fitness_certificate_front_side_img_path', 'license_expire_date', 'insurence_expire_date', 'fitness_certificate_expire_date', 'vehicle__permit_expire_date', 'vehicle__rc_expire_date', 'vehicle__emission_test_expire_date','vehicle__vehicletypes__vehicle_type_name','vehicle__vehicletypes__id','vehicle__vehicletypes__vehicle_type_image', 'user__profile_image', 'vehicle__is_active', 'driver_status')
            
            driver_image_obj_img = Driver.objects.get(user_id=request.query_params['user_id'])
            live_url = "https://logistics.thestorywallcafe.com/media"

            imagesDict = {
                "license_img_front": base64.b64encode(requests.get(live_url + str(driver_image_obj_img.license_img_front)).content),
                "license_img_back": base64.b64encode(requests.get(live_url + str(driver_image_obj_img.license_img_back)).content),
                "passbook_img": base64.b64encode(requests.get(live_url + str(driver_image_obj_img.passbook_img)).content)
            }

            # print("owner id============>", driver_obj[0]['owner_id'])

            if driver_obj[0]['owner_id'] == request.query_params['user_id']:
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

                return Response({'data': obj_with_owner_details, 'base64ImageData': imagesDict})
            else:
                # print("printing in else block")

                obj_with_owner_details = list(driver_obj)
                print("obj_with_owner_details==>>>", obj_with_owner_details)
                if obj_with_owner_details[0]['user__profile_image'] == "":
                    obj_with_owner_details[0]['user__profile_image'] = None

                owner_details = CustomUser.objects.filter(id=driver_obj[0]['owner_id']).values().first()

                # print("query==>", Driver.objects.filter(owner_id=driver_obj[0]['owner_id']).values('driver_driving_license'))

               
                owner_licence_number = Driver.objects.filter(owner_id=driver_obj[0]['owner_id']).values('owner_driving_licence').first()
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
                if Driver.objects.get(user_id=request.query_params['user_id']).owner_id is None:
                    obj_with_owner_details[0]['owner_details'] = None
                else:
                    obj_with_owner_details[0]['owner_details'] = [owner_details]

                return Response({'data': obj_with_owner_details, 'base64ImageData': imagesDict})
        else:
            driver_obj = Driver.objects.all().values('user_id', 'vehicle_id','vehicle__vehicle_name', 'vehicle__vehicle_number', 'driver_driving_license', 'user__first_name', 'badge', 'user__adhar_card_front_side_img_path', 'user__adhar_card_back_side_img_path', 'user__role__user_role_name', 'user__mobile_number', 'driver_driving_license', 'vehicle__permit_front_side_img_path', 'vehicle__registration_certificate_front_side_img_path', 'vehicle__vehicle_status','vehicle__registration_certificate_back_side_img_path', 'vehicle__pollution_certificate_front_side_img_path', 'license_img_front', 'license_img_back', 'insurence_img', 'passbook_img', 'license_expire_date', 'insurence_expire_date', 'fitness_certificate_expire_date', 'vehicle__permit_expire_date', 'vehicle__rc_expire_date', 'vehicle__emission_test_expire_date', 'vehicle__is_active', 'driver_status')
            return Response({'data': driver_obj})

    def post(self,request):
        data = request.data

        full_name = data['full_name']
        driving_licence_number = data['driving_licence_number']
        badge = data['badge']
        adhar_front_image = data['adhar_front_image']
        adhar_back_image = data['adhar_back_image']
        licence_image_front = data['licence_image_front']
        licence_image_back = data['licence_image_back']
        passbook_image = data['passbook_image']
        owner_details = data['owner_details']
        driver_id = data['driver_id']
        is_online=data.get('is_online')



        if licence_image_front is not None or licence_image_back is not None:
            # print("base 64 byte==>", len(adhar_front_image) * 3 / 4 - adhar_front_image.count('='))
            file_size = file_size = len(adhar_front_image) * 3 / 4 - adhar_front_image.count('=')
            # print("total mb==>>", int(file_size) / 1000000)

        if (adhar_front_image is not None
            or adhar_back_image is not None
            or passbook_image is not None
            or licence_image_front is not None):

            converted_af_image = convertBase64(adhar_front_image, 'adharFront', driver_id, 'documents')
            converted_ab_image = convertBase64(adhar_back_image, 'adharBack', driver_id, 'documents')
            converted_licence_image_front = convertBase64(licence_image_front, 'licencefront', driver_id, 'driving_license_file')
            converted_licence_image_back = convertBase64(licence_image_back, 'licenceback', driver_id, 'driving_license_file')
            converted_passbook_image = convertBase64(passbook_image, 'passbook', driver_id, 'passbooks')

            Driver.objects.filter(user_id=driver_id).update(
                owner_id=driver_id,
                badge=badge,
                driver_driving_license=driving_licence_number,
                license_img_front=converted_licence_image_front,
                license_img_back=converted_licence_image_back,
                passbook_img=converted_passbook_image,
                driver_status = "Driver Details Entered with Mobile Number"
            )

            CustomUser.objects.filter(id=driver_id).update(
                adhar_card_front_side_img_path=converted_af_image,
                adhar_card_back_side_img_path=converted_ab_image,
                first_name=full_name,
                role_id=3
            )

        if isinstance(owner_details, dict):
            converted_owneraf_image = convertBase64(owner_details.get('owner_adhar_front_image'), 'owner_adharFront', driver_id, 'documents')
            converted_ownerab_image = convertBase64(owner_details.get('owner_adhar_back_image'), 'owner_adharBack', driver_id, 'documents')
            owner_obj = CustomUser.objects.create(
                adhar_card_front_side_img_path=converted_owneraf_image,
                adhar_card_back_side_img_path=converted_ownerab_image,
                first_name=owner_details.get('owner_name'),
                role_id=4,
                mobile_number=owner_details.get('owner_mobile_number'),
            )
            driver_driving_license = owner_details.get('owner_drivering_licence_number', '')
            owner_id = owner_obj.id if owner_obj else None
            Driver.objects.filter(user_id=driver_id).update(owner_id=owner_id, owner_driving_licence=owner_details.get('owner_drivering_licence_number'))


        return Response({'success': True})

    def put(self, request, driver_id):
        data = request.data

        full_name = data['full_name']
        driving_licence_number = data['driving_licence_number']
        badge = data['badge']
        # driver_mobile_number = data['driver_mobile_number']
        adhar_front_image = data['adhar_front_image']
        adhar_back_image = data['adhar_back_image']
        licence_image_front = data['licence_image_front']
        licence_image_back = data['licence_image_back']
        passbook_image = data['passbook_image']
        mobile_number = data['mobile_number']
        owner_details = data['owner_details']  
        if data['profile_image']:
            if data['profile_image']:
                if "data:image/" in data['profile_image']:
                    converted_profile_image = convertBase64(data['profile_image'], 'driver_profile_image', uuid.uuid4(), 'profile')
                    CustomUser.objects.filter(id=driver_id).update(profile_image=converted_profile_image)
                    driver = CustomUser.objects.get(id=driver_id)
                    response_data = {
                        'message': 'Driver profile image is updated',
                        'profile_image_path': driver.profile_image.url,
                    }
                    # print('response_data=============',response_data)
                    return Response(response_data)  
                else:
                    pass 

        if adhar_front_image or adhar_back_image is not None or passbook_image is not None or licence_image is not None:
            if "data:image/" in adhar_front_image:
                converted_af_image = convertBase64(adhar_front_image, 'adharFront', uuid.uuid4(), 'documents')
                CustomUser.objects.filter(id=driver_id).update(adhar_card_front_side_img_path = converted_af_image)
            else:
                pass
            if "data:image/" in adhar_back_image:
                converted_ab_image = convertBase64(adhar_back_image, 'adharBack', uuid.uuid4(), 'documents')
                CustomUser.objects.filter(id=driver_id).update(adhar_card_back_side_img_path = converted_ab_image)
            else:
                pass
            if "data:image/" in licence_image_front:
                converted_licence_image_front = convertBase64(licence_image_front, 'licencefront', uuid.uuid4(), 'driving_license_file')
                Driver.objects.filter(user_id=driver_id).update(license_img_front = converted_licence_image_front)
            else:
                pass
            if "data:image/" in licence_image_back:
                converted_licence_image_back = convertBase64(licence_image_back, 'licenceback', uuid.uuid4(), 'driving_license_file')
                Driver.objects.filter(user_id=driver_id).update(license_img_back = converted_licence_image_back)
            else:
                pass
            if "data:image/" in passbook_image:
                converted_passbook_image = convertBase64(passbook_image, 'passbook', uuid.uuid4(), 'passbooks')
                Driver.objects.filter(user_id=driver_id).update(passbook_img = converted_passbook_image)
            else:
                pass

        # if data['owner_details'] is not None:
        #     if data['owner_details']['owner_id'] is None:
        #         if data.get('updated_by'):
        #             pass
        #         else:
        #             Driver.objects.filter(user_id=driver_id).update(
        #                 owner_id=driver_id,
        #                 badge=badge,
        #                 driver_driving_license=driving_licence_number,
        #                 driver_status = "waiting for verification"
        #             )

        #         CustomUser.objects.filter(id=driver_id).update(
        #             first_name=full_name,
        #             role_id=3
        #         )

        # else:
        #     if data.get('updated_by'):
        #         pass
        #     else:
        #         Driver.objects.filter(user_id=driver_id).update(
        #             owner_id=driver_id,
        #             driver_status = "waiting for verification",
        #             badge=badge,
        #             driver_driving_license=driving_licence_number,
        #         )
        #         CustomUser.objects.filter(id=driver_id).update(first_name=full_name,)

        if owner_details is not None:
            if data['owner_details']['owner_id'] is not None:
                if "data:image/" in data['owner_details']['owner_adhar_front_image'] or data['owner_details']['owner_adhar_front_image'] == "":
                    converted_owneraf_image = convertBase64(data['owner_details']['owner_adhar_front_image'], 'owner_adharFront', driver_id, 'documents')
                    CustomUser.objects.filter(id=data['owner_details']['owner_id']).update(adhar_card_front_side_img_path=converted_owneraf_image)
                else:
                    pass
                if "data:image/" in data['owner_details']['owner_adhar_back_image'] or data['owner_details']['owner_adhar_back_image'] == "":
                    converted_ownerab_image = convertBase64(data['owner_details']['owner_adhar_back_image'], 'owner_adharBack', driver_id, 'documents')
                    CustomUser.objects.filter(id=data['owner_details']['owner_id']).update(adhar_card_back_side_img_path=converted_ownerab_image)
                else:
                    pass

                if data.get('updated_by'):
                    owner_obj = CustomUser.objects.filter(id=data['owner_details']['owner_id']).update(
                        first_name=data['owner_details']['owner_name'],
                        role_id=4,
                        mobile_number=data['owner_details']['owner_mobile_number'],
                    )

                    Driver.objects.filter(owner_id=data['owner_details']['owner_id']).update(owner_driving_licence=data['owner_details']['owner_drivering_licence_number'])
                else:
                    owner_obj = CustomUser.objects.filter(id=data['owner_details']['owner_id']).update(
                        first_name=data['owner_details']['owner_name'],
                        role_id=4,
                        mobile_number=data['owner_details']['owner_mobile_number'],
                    )

                    Driver.objects.filter(owner_id=data['owner_details']['owner_id']).update(owner_driving_licence=data['owner_details']['owner_drivering_licence_number'], driver_status = "waiting for verification")

            else:
                converted_owneraf_image = convertBase64(data['owner_details']['owner_adhar_front_image'], 'owner_adharFront', driver_id, 'documents')
                converted_ownerab_image = convertBase64(data['owner_details']['owner_adhar_back_image'], 'owner_adharBack', driver_id, 'documents')

                if data.get('updated_by'):
                    owner_obj = CustomUser.objects.create(
                        adhar_card_front_side_img_path=converted_owneraf_image,
                        adhar_card_back_side_img_path=converted_ownerab_image,
                        first_name=data['owner_details']['owner_name'],
                        role_id=4,
                        mobile_number=data['owner_details']['owner_mobile_number'],
                    )

                    
                    Driver.objects.filter(user_id=driver_id).update(owner_driving_licence=data['owner_details']['owner_drivering_licence_number'], owner_id=owner_obj.id)
                else:
                    owner_obj = CustomUser.objects.create(
                        adhar_card_front_side_img_path=converted_owneraf_image,
                        adhar_card_back_side_img_path=converted_ownerab_image,
                        first_name=data['owner_details']['owner_name'],
                        role_id=4,
                        mobile_number=data['owner_details']['owner_mobile_number'],
                    )

                    
                    Driver.objects.filter(user_id=driver_id).update(owner_driving_licence=data['owner_details']['owner_drivering_licence_number'], owner_id=owner_obj.id, driver_status = "waiting for verification")

        else:
            Driver.objects.filter(user_id=driver_id).update(owner_id=None)

        driver = Driver.objects.get(user_id=driver_id)
        vehicle = driver.vehicle
        vehicle.vehicle_status = "waiting for verification"
        vehicle.save()

        return Response({'message': 'driver updated successfully'})

class BookingVehicleApi(APIView):
    def post(self, request):
        data = request.data

        # from_location = data['from_location']
        # to_location = data['to_location']
        vehicle_reg_number = data['vehicle_reg_number']
        user_id = data['user_id']
        location_details = data['location_details']
       

        user_obj = CustomUser.objects.filter(id=user_id)

        if vehicle_reg_number is not None:
            vehicle_obj = Vehicle.objects.filter(vehicle_number=vehicle_reg_number).values()

            order_obj = OrderDeatil.objects.create(
                # from_location = from_location,
                # to_location = to_location,
                user_id__id = user_id ,
                vehicle_number = vehicle_reg_number,
                location_details = location_details,
            )

            driver_obj =  Driver.objects.get(vehicle__vehicle_number=vehicle_reg_number)

            BookingDetail.objects.create(order_id_id=order_obj.id, driver_id_id=driver_obj.id)

            return Response({'message': data, 'user_data': user_obj.values('first_name','last_name','mobile_number','email','alternate_number')})
        else:
            pass

from userModule.models import *
import ast
class OrderDeatilAPI(APIView):
    def get(self,request,user_id):
        data=request.data
        order_details = BookingDetail.objects.filter(driver_id=user_id).reverse().values('order_id__location_details','total_amount','order_id__user_id__mobile_number', 'order_id__user_id__alternate_number','status__colour','driver__mobile_number')
        return Response(order_details)

    def get(self,request):
        data = request.data
        is_scheduled = request.query_params.get('is_scheduled')
        status_id = request.query_params.get('status_id')
        # status_id_list = re.findall(r'\d+', status_id)
        # print(type(status_id_list))
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        today = date.today()
        # return Response([])
        # book_obj=BookingDetail.objects.all().values()
        # print('book_obj====',book_obj)

        if is_scheduled and status_id and status_id and end_date :
            status_id_list = re.findall(r'\d+', status_id)
            status_id_list = [int(num) for num in status_id_list]
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            end_date = end_date + datetime.timedelta(days=1)
            is_scheduled = True if is_scheduled.lower() == 'true' else False
            msg_obj = BookingDetail.objects.filter(Q(ordered_time__gte=start_date) &Q(ordered_time__lte=end_date) &Q(status__id__in=status_id_list) &Q(is_scheduled=is_scheduled)).values(
                'id', 'order__user_id', 'order_id', 'driver_id', 'status','order__vehicle_number', 'total_amount','order__user_id__first_name', 'order__user_id__mobile_number',
                'status__status_name', 'order__otp','driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp', 'driver__first_name','status__colour','driver__mobile_number', 'ordered_time', 'is_scheduled','scheduledorder__scheduled_date_and_time','total_amount_without_actual_time_taken', 'driver__vehicle__vehicle_number')
            # print('msg=====',msg_obj)
            reverse_obj=reversed(msg_obj)
            return Response(reverse_obj)

        if status_id and start_date and end_date:
            status_id_list = re.findall(r'\d+', status_id)
            status_id_list = [int(num) for num in status_id_list]
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            end_date = end_date + datetime.timedelta(days=1)
            msg_obj = BookingDetail.objects.filter(Q(ordered_time__gte=start_date) &Q(ordered_time__lte=end_date) &Q(status__id__in=status_id_list)).values(
                'id', 'order__user_id', 'order_id', 'driver_id', 'status','order__vehicle_number', 'total_amount','order__user_id__first_name', 'order__user_id__mobile_number',
                'status__status_name', 'order__otp','driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp', 'driver__first_name','status__colour','driver__mobile_number', 'ordered_time', 'is_scheduled','scheduledorder__scheduled_date_and_time','total_amount_without_actual_time_taken', 'driver__vehicle__vehicle_number')
            # print('msg=====',msg_obj)
            reverse_obj=reversed(msg_obj)
            return Response(reverse_obj)

        if is_scheduled and start_date and end_date:
            is_scheduled = True if is_scheduled.lower() == 'true' else False
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            end_date = end_date + datetime.timedelta(days=1)
            msg_obj = BookingDetail.objects.filter(Q(ordered_time__gte=start_date) &Q(ordered_time__lte=end_date) &Q(is_scheduled=is_scheduled)).values(
                'id', 'order__user_id', 'order_id', 'driver_id', 'status','order__vehicle_number', 'total_amount','order__user_id__first_name', 'order__user_id__mobile_number',
                'status__status_name', 'order__otp','driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp', 'driver__first_name','status__colour','driver__mobile_number', 'ordered_time', 'is_scheduled','scheduledorder__scheduled_date_and_time','total_amount_without_actual_time_taken', 'driver__vehicle__vehicle_number')
            # print('msg=====',msg_obj)
            reverse_obj=reversed(msg_obj)
            return Response(reverse_obj)

        if start_date and end_date:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            end_date = end_date + datetime.timedelta(days=1)
            msg_obj = BookingDetail.objects.filter(Q(ordered_time__gte=start_date) &Q(ordered_time__lte=end_date)).values(
                'id', 'order__user_id', 'order_id', 'driver_id', 'status','order__vehicle_number', 'total_amount','order__user_id__first_name', 'order__user_id__mobile_number',
                'status__status_name', 'order__otp','driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp', 'driver__first_name','status__colour','driver__mobile_number', 'ordered_time', 'is_scheduled','scheduledorder__scheduled_date_and_time','total_amount_without_actual_time_taken', 'driver__vehicle__vehicle_number')
            # print('msg=====',msg_obj)
            reverse_obj=reversed(msg_obj)
            return Response(reverse_obj)

        if status_id and is_scheduled:
            status_id_list = re.findall(r'\d+', status_id)
            status_id_list = [int(num) for num in status_id_list]
            is_scheduled = True if is_scheduled.lower() == 'true' else False
            msg_obj = BookingDetail.objects.filter(Q(status__id__in=status_id_list)&Q(is_scheduled = is_scheduled)).values('id','order__user_id','order_id','driver_id', 'status', 'order__vehicle_number','total_amount','order__user_id__first_name','order__user_id__mobile_number', 'status__status_name', 'order__otp', 'driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp','driver__first_name','status__colour','driver__mobile_number','ordered_time','is_scheduled','scheduledorder__scheduled_date_and_time','total_amount_without_actual_time_taken', 'driver__vehicle__vehicle_number')
            reverse_obj=reversed(msg_obj)
            return Response(reverse_obj)

        if status_id:
            status_id_list = re.findall(r'\d+', status_id)
            status_id_list = [int(num) for num in status_id_list]
            msg_obj = BookingDetail.objects.filter(Q(status__id__in=status_id_list)).values('id','order__user_id','order_id','driver_id', 'status', 'order__vehicle_number','total_amount','order__user_id__first_name','order__user_id__mobile_number', 'status__status_name', 'order__otp', 'driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp','driver__first_name','status__colour','driver__mobile_number','ordered_time','is_scheduled','scheduledorder__scheduled_date_and_time','total_amount_without_actual_time_taken', 'driver__vehicle__vehicle_number')
            reverse_obj=reversed(msg_obj)
            return Response(reverse_obj)

        if is_scheduled:
            is_scheduled = True if is_scheduled.lower() == 'true' else False
            msg_obj = BookingDetail.objects.filter(is_scheduled = is_scheduled).values('id','order__user_id','order_id','driver_id', 'status', 'order__vehicle_number','total_amount','order__user_id__first_name','order__user_id__mobile_number', 'status__status_name', 'order__otp', 'driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp','driver__first_name','status__colour','driver__mobile_number','ordered_time','is_scheduled','scheduledorder__scheduled_date_and_time','total_amount_without_actual_time_taken', 'driver__vehicle__vehicle_number')
            reverse_obj=reversed(msg_obj)
            return Response(reverse_obj)

        order_detail = BookingDetail.objects.all().order_by('-id').values('id','order__user_id','order_id','driver_id', 'status', 'order__vehicle_number','total_amount','order__user_id__first_name','order__user_id__mobile_number', 'status__status_name', 'order__otp', 'driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp','driver__first_name','status__colour','ordered_time','driver__mobile_number','scheduledorder__scheduled_date_and_time','total_amount_without_actual_time_taken','driver__vehicle__vehicle_number')
        return Response(order_detail)




        # order_detail = BookingDetail.objects.filter(ordered_time__date=today).values('id','order__user_id','order_id','driver_id', 'status', 'order__vehicle_number','total_amount','order__user_id__first_name','order__user_id__mobile_number', 'status__status_name', 'order__otp', 'driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp','driver__first_name','status__colour','ordered_time','driver__mobile_number','scheduledorder__scheduled_date_and_time')
        # reverse_obj=reversed(order_detail)
        # return Response([])


        # order_detail = BookingDetail.objects.all().values('id','order__user_id','order_id','driver_id', 'status', 'order__vehicle_number','total_amount','order__user_id__first_name','order__user_id__mobile_number', 'status__status_name', 'order__otp', 'driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp','driver__first_name','status__colour','driver__mobile_number')
        # reverse_obj=reversed(order_detail)
        # return Response(reverse_obj)
        # if driver_id:
        #     msg_obj = Customised_message.objects.filter(driver__user__id = driver_id).values().last()
        #     return Response({'data':msg_obj})
        # else:
        #     msg_obj = Customised_message.objects.all().values()
        #     return Response({'data':msg_obj})

    # def post(self,request):
        # data=request.data
        # status_id=data['status_id']
        # start_date=data['start_date']
        # end_date=data['end_date']
        # is_scheduled=data['is_scheduled']
        # ordered_times=data.get('ordered_time')
        # end_date_plus_one = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        # order_status_count = BookingDetail.objects.filter(Q(ordered_time__range=(start_date, end_date_plus_one)|Q(status_id__in=status_id)|Q(is_scheduled=False))).values(
        #     'id',
        #     'order__user_id__first_name',
        #     'order__user_id__mobile_number',
        #     'status__colour',
        #     'status__status_name',
        #     'driver__first_name',
        #     'driver__mobile_number',
        #     'ordered_time',
        #     'last_update_timestamp',
        #     'order_id',
        #     'order__vehicle_number',
        #     'is_scheduled'
        # )
        # reverse_obj=reversed(order_status_count)
        # print('order_status_count=======>>>>>>',order_status_count)

        # return Response(reverse_obj)

        # data = request.data
        # status_id = data.get('status_id')
        # is_scheduled = data.get('is_scheduled')
        # ordered_times = data.get('ordered_time')

        # q_obj = Q(is_scheduled=False)

        # if status_id:
        #     q_obj |= Q(status_id__in=status_id)

        # if ordered_times:
        #     start_date = ordered_times.get('start_date')
        #     end_date = ordered_times.get('end_date')
        #     if start_date and end_date:
        #         end_date_plus_one = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        #         q_obj |= Q(ordered_time__range=(start_date, end_date_plus_one))

        # order_status_count = BookingDetail.objects.filter(q_obj).values(
        #     'id',
        #     'order__user_id__first_name',
        #     'order__user_id__mobile_number',
        #     'status__colour',
        #     'status__status_name',
        #     'driver__first_name',
        #     'driver__mobile_number',
        #     'ordered_time',
        #     'last_update_timestamp',
        #     'order_id',
        #     'order__vehicle_number',
        #     'is_scheduled'
        # ).order_by('-id')

        # return Response(order_status_count)


        # data = request.data
        # status_id = data.get('status_id')
        # start_date = data.get('start_date')
        # end_date = data.get('end_date')
        # is_scheduled = data.get('is_scheduled')
        # ordered_time = data.get('ordered_time')
        
        # # Convert end_date to datetime object and add 1 day to include end_date in the range
        # end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)

        # # Create a list of Q objects for filtering
        # filter_list = [Q(ordered_time__range=(start_date, end_date_obj))]
        
        # if status_id:
        #     filter_list.append(Q(status_id__in=status_id))
        
        # if is_scheduled is not None:
        #     filter_list.append(Q(is_scheduled=is_scheduled))
        
        # if ordered_time:
        #     filter_list.append(Q(ordered_time=ordered_time))

        # order_status_count = BookingDetail.objects.filter(
        #     *filter_list
        # ).values(
        #     'id',
        #     'order__user_id__first_name',
        #     'order__user_id__mobile_number',
        #     'status__colour',
        #     'status__status_name',
        #     'driver__first_name',
        #     'driver__mobile_number',
        #     'ordered_time',
        #     'last_update_timestamp',
        #     'order_id',
        #     'order__vehicle_number',
        #     'is_scheduled'
        # ).order_by('-ordered_time')

        # return Response(order_status_count)


        # data = request.data
        # status_id = data.get('status_id')
        # start_date = data.get('start_date')
        # end_date = data.get('end_date')
        # is_scheduled = data.get('is_scheduled')

        # # Convert end_date to a datetime object and add one day
        # end_date_plus_one = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)

        # orders = BookingDetail.objects.all()

        # if status_id:
        #     orders = orders.filter(status_id__in=status_id)

        # if start_date:
        #     orders = orders.filter(ordered_time__gte=start_date)

        # if end_date:
        #     orders = orders.filter(ordered_time__lt=end_date_plus_one)

        # if is_scheduled is not None:
        #     orders = orders.filter(is_scheduled=is_scheduled)

        # order_status_count = orders.values(
        #     'id',
        #     'order__user_id__first_name',
        #     'order__user_id__mobile_number',
        #     'status__colour',
        #     'status__status_name',
        #     'driver__first_name',
        #     'driver__mobile_number',
        #     'ordered_time',
        #     'last_update_timestamp',
        #     'order_id',
        #     'order__vehicle_number',
        #     'is_scheduled'
        # ).order_by('-id')

        # return Response(order_status_count)

        # data=request.data

        # id = request.query_params.get('id')
        # if id:
        #     all_data = BookingDetail.objects.filter(id=id).values('order_id__location_details','order_id__user_id__mobile_number', 'order_id__user_id__alternate_number')

        #     if not all_data:
        #         return Response({
        #         'error':{'message':'Record not found!',
        #         'status_code':status.HTTP_404_NOT_FOUND,
        #         }},status=status.HTTP_404_NOT_FOUND)
        #     return Response({'result':{'status':'GET by Id','data':all_data}})


        # else:
        #     all_data = BookingDetail.objects.all().values('order__user_id','order_id','driver_id','status', 'order__vehicle_number','status__status_name','order__otp', 'driver__vehicle__vehicle_name', 'order__total_estimated_cost', 'last_update_timestamp','order__user_id__first_name','order__user_id__mobile_number')
        #     return Response({'result':{'status':'GET','data':all_data}})
# 'driver__user__first_name', 'driver__user__mobile_number', 'order__otp', 'driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp
    # def get(self, request, user_id):
        
    def delete(self,request,pk):
        if OrderDetails.objects.filter(id=pk).exists():
            OrderDetails.objects.filter(id=pk).delete()

            return Response({'Results':'order_details deleted successfully'})
        return Response({'order_id not found to delete'})


class CancellationApi(APIView):
    def post(self,request):
        data = request.data

        booking_id = data['booking_id']
        status_id = data['status_id']
        if BookingDetail.objects.filter(id=booking_id).exists():
            # print('aaaaaaaaaaaaaaa')
            BookingDetail.objects.get(id=booking_id).update(status_id_id=status_id)
            return Response({'message':"Your order is Cancelled!!"})
        else:
            return Response({'message': "Booking id not found"})

class User_feedback(APIView):
    def post(self,request):
        data =  request.data

        user_id = data.get('user_id')
        rating = data.get('rating')
        review = data.get('review')
        order_id = data.get('order_id')
        # print('aaaaaaaaa')

        if OrderDetails.objects.filter(id=data['order_id']).exists():
            # print('SSSSSSSSSSSSSSSS')
            user_feedback = UserFeedback.objects.create(user_id=data['user_id'],rating=data['rating'],review=data['review'],order_id=data['order_id'])
            return Response({'message': 'Thank you for the feedback'})
        else:
            return Response({'error':'order_id is not found'},status=status.HTTP_404_NOT_FOUND)


        

            
# from geopy.geocoders import Nominatim

# geolocator = Nominatim(user_agent="geoapi")

# Latitude = "13.0661109"
# Longitude = "77.5797956"return Response({'message': data, 'user_data': user_obj.values('first_name','last_name','mobile_number','email','alternate_number')})

# location = geolocator.reverse(Latitude+","+Longitude)

# location = geolocator.geocode(Latitude+","+Longitude)


# print("location==>>",location.raw['address'])

class Customised_messageApi(APIView):
    def get(self,request):
        data = request.data
        message_type = request.query_params.get('message_type')
        id = request.query_params.get('id')
        driver_id = request.query_params.get('driver_id')
        if id:
            msg_obj = Customised_message.objects.filter(id = id).values()
            return Response({'data':msg_obj})
        if driver_id:
            msg_obj = Customised_message.objects.filter(driver__user__id = driver_id).values().last()
            return Response({'data':msg_obj})
        else:
            msg_obj = Customised_message.objects.all().values()
            return Response({'data':msg_obj})

    #     id = request.query_params.get('id')
    #     if id:
    #         all_data = Customised_message.objects.filter(id=id).values()

    #         if not all_data:
    #             return Response({
    #             'error':{'message':'Record not found!',
    #             'status_code':status.HTTP_404_NOT_FOUND,
    #             }},status=status.HTTP_404_NOT_FOUND)
    #         return Response({'result':{'status':'GET by Id','data':all_data}})


    #     else:
    #         all_data = Customised_message.objects.all().values()
    #         return Response({'result':{'status':'GET','data':all_data}})

    def post(self,request):
        data = request.data
        driver_id = request.query_params.get('driver_id')
        message_type=data['message_type']
        driver__user__id=data.get('driver__user__id') 
        if Driver.objects.filter(user__id=driver_id).exists():
            # print("ssssssssssss",user__id)
            # print("ppppppppppppp",driver_id)
            msg_obj= Customised_message.objects.create(message_type=message_type,driver__user__id=driver_id)
            return Response({'data':'default_message Successfully Added!!'})
        else:
            return Response({'error':'driver_id is not found'},status=status.HTTP_404_NOT_FOUND)

    def put(self,request,pk):
        data = request.data
        driver_id=data['driver_id']
        message_type=data['message_type']
        if Customised_message.objects.filter(id=pk).exists():
            Customised_message.objects.filter(id=pk).update(message_type=message_type,driver_id=driver_id)
            return Response({'message': 'message is updated'})
        else:
            return Response({'error':'id is not found'},status=status.HTTP_404_NOT_FOUND)


    def delete(self,request,pk):
        data = request.data
        if Customised_message.objects.filter(id=pk).exists():
            Customised_message.objects.filter(id=pk).delete()
            return Response({'message': 'message is deleted'})
        else:
            return Response({'error':'id is not found'},status=status.HTTP_404_NOT_FOUND)

    
class accept_or_declineApi(APIView):
    def put(self,request,pk):
        data = request.data
        vehicle_status=data['vehicle_status']

        if Driver.objects.filter(user_id=pk).exists():            
            driver_obj = Driver.objects.get(user_id=pk)
            # print('SSSSSSSSSSSS',driver_obj)
            Driver.objects.filter(user_id=pk).update(driver_status=vehicle_status)
            Vehicle.objects.filter(id=driver_obj.vehicle_id).update(vehicle_status=vehicle_status)
            return Response({'message': 'message is updated'})
        else:
            return Response({'error':'id is not found'},status=status.HTTP_404_NOT_FOUND)

class ScheduledOrder_countApi(APIView):
    def get(self,request):
        is_scheduled = request.query_params.get('is_scheduled')
        date = request.query_params.get('date')
        scheduled_date_and_time = request.query_params.get('scheduled_date_and_time')
        if is_scheduled and date:
            count=0
            matching_orders = []
            bookings=BookingDetail.objects.filter(is_scheduled=is_scheduled).values('id','order__user_id__first_name','order__user_id__mobile_number','status__colour','status__status_name','driver__first_name','driver__mobile_number','ordered_time','last_update_timestamp','order_id','order__vehicle_number','ordered_time','total_amount_without_actual_time_taken','scheduledorder__scheduled_date_and_time','order__total_estimated_cost')
            for i in bookings:
                if i['scheduledorder__scheduled_date_and_time'] and str(i['scheduledorder__scheduled_date_and_time'].date()) == date:
                    count+=1
                    matching_orders.append(i)
            return Response({'count': count, 'Booking_Detail': matching_orders})
        if is_scheduled:
            bookings = BookingDetail.objects.filter(
                is_scheduled=is_scheduled,
                scheduledorder__scheduled_date_and_time=scheduled_date_and_time
            ).values('id', 'order__user_id__first_name','order__user_id__mobile_number','status__colour','status__status_name','driver__first_name','driver__mobile_number','ordered_time','last_update_timestamp','order_id','order__vehicle_number','ordered_time','total_amount_without_actual_time_taken','scheduledorder__scheduled_date_and_time','order__total_estimated_cost')
            count = bookings.count()
            return Response({'count': count, 'Booking_Detail': bookings})
        return Response({'message': 'Invalid parameters'})

class Order_dashboardApi(APIView):
    def get(self,request):
        ordered_time = request.query_params.get('ordered_time')
        
        bookings = BookingDetail.objects.all().values('id','order__user_id__first_name','order__user_id__mobile_number','status__colour','status__status_name','driver__first_name','driver__mobile_number','ordered_time','last_update_timestamp','order_id','order__vehicle_number','ordered_time','total_amount_without_actual_time_taken','scheduledorder__scheduled_date_and_time','order__total_estimated_cost')
        
        if ordered_time:
            matched_bookings = []
            for booking in bookings:
                if booking['ordered_time'] and str(booking['ordered_time'].date()) == ordered_time:
                    matched_bookings.append(booking)
            return Response({'count': len(matched_bookings), 'bookings_Detail': matched_bookings})
        else:
            return Response({'count': bookings.count(), 'bookings_Detail': bookings})

    # def post(self,request):

        # data = request.data
        # ordered_time=data.get('ordered_time')
        # print('AAAAA',BookingDetail.objects.all().values('ordered_time'))
        
        # data_s = BookingDetail.objects.all().values('ordered_time')
        
        # dateList = []
        
        # for i in data_s:
        #     if ordered_time == str(i['ordered_time'].date()):
        #         dateList.append(str(i['ordered_time'].date()))
        # return Response({'message': len(dateList)})
       
from django.utils import timezone
from rest_framework.response import Response


# import datetime

class DriverCountStatusApi(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        is_online = request.query_params.get('is_online')
        date_online = request.query_params.get('date_online')
        date_offline = request.query_params.get('date_offline')
        drivers_detail = None
        drivers_count = 0
        
        if is_online and date:
            is_online = True if is_online.lower() == 'true' else False
            drivers_detail = Driver.objects.filter(
                is_online=is_online
            ).values(
                'id','vehicle_id','vehicle__vehicle_status','vehicle__vehicle_name', 'vehicle__vehicle_number', 'driver_driving_license', 'user__first_name', 'badge', 'user__adhar_card_front_side_img_path', 'user__adhar_card_back_side_img_path', 'user__role__user_role_name', 'user__mobile_number', 'vehicle__permit_front_side_img_path', 'vehicle__registration_certificate_front_side_img_path', 'vehicle__registration_certificate_back_side_img_path', 'vehicle__pollution_certificate_front_side_img_path', 'license_img_front', 'license_img_back', 'insurence_img', 'passbook_img', 'user_id', 'owner_id', 'fitness_certificate_back_side_img_path','fitness_certificate_front_side_img_path', 'license_expire_date', 'insurence_expire_date', 'fitness_certificate_expire_date', 'vehicle__permit_expire_date', 'vehicle__rc_expire_date', 'vehicle__emission_test_expire_date','vehicle__vehicletypes__vehicle_type_name','vehicle__vehicletypes__id','vehicle__vehicletypes__vehicle_type_image', 'user__profile_image', 'vehicle__is_active','is_online', 'date_online','date_offline', 'driver_status'
            )
            
            tempList = []
            if drivers_detail is not None:
                for driver in drivers_detail:
                    if is_online:
                        if driver['date_online'] is not None and str(driver['date_online'].date()) == date:
                            tempList.append(driver)
                    else:
                        if driver['date_offline'] is not None and str(driver['date_offline'].date()) == date:
                            tempList.append(driver)
            drivers_count = len(tempList)
            return Response({'driver_detail': tempList, 'count': drivers_count})

        if is_online:
            is_online = True if is_online.lower() == 'true' else False
            drivers_detail = Driver.objects.filter(
                is_online=is_online
            ).values(
                'id','vehicle_id','vehicle__vehicle_status','vehicle__vehicle_name', 'vehicle__vehicle_number', 'driver_driving_license', 'user__first_name', 'badge', 'user__adhar_card_front_side_img_path', 'user__adhar_card_back_side_img_path', 'user__role__user_role_name', 'user__mobile_number', 'vehicle__permit_front_side_img_path', 'vehicle__registration_certificate_front_side_img_path', 'vehicle__registration_certificate_back_side_img_path', 'vehicle__pollution_certificate_front_side_img_path', 'license_img_front', 'license_img_back', 'insurence_img', 'passbook_img', 'user_id', 'owner_id', 'fitness_certificate_back_side_img_path','fitness_certificate_front_side_img_path', 'license_expire_date', 'insurence_expire_date', 'fitness_certificate_expire_date', 'vehicle__permit_expire_date', 'vehicle__rc_expire_date', 'vehicle__emission_test_expire_date','vehicle__vehicletypes__vehicle_type_name','vehicle__vehicletypes__id','vehicle__vehicletypes__vehicle_type_image', 'user__profile_image', 'vehicle__is_active', 'is_online','date_online','date_offline', 'driver_status'
            )
            count=drivers_detail.count()
        return Response({'drivers_detail':drivers_detail,'count':count})



import datetime
from django.db.models.functions import Extract
import pandas as pd
import calendar

class Filter_OrdersApi(APIView):            
    def post(self,request):
        data = request.data
        date = data['date']
        # month=data['month']
        is_days = data['is_days']
        is_month = data['is_month']
        current_time = datetime.datetime.now()
        # print("current_time===>", current_time.day)

        tempDaysorMonth = []
        tempDaysDictorMonth = {}
        # order_obj = BookingDetail.objects.all().values('ordered_time__day','ordered_time__month').last() #local
        order_obj = BookingDetail.objects.all().values('ordered_time').latest('id') #server    
        if is_days ==True:
            d = pd.Timestamp(date)
            # print("==<>>",d.date())
            if int(d.day) == current_time.day:
                tempDaysDictorMonth['day'] = current_time.day
                tempDaysDictorMonth['count'] = BookingDetail.objects.filter(ordered_time__date=date).count()
                tempDaysorMonth.append(tempDaysDictorMonth)
                tempDaysDictorMonth = {}
            else:
                size = len(date) 
                for j in range(d.day, order_obj['ordered_time'].date().day + 1)[:5]:  #server
                # for j in range(d.day, order_obj['ordered_time__day']+1)[:5]: #local
                    replacement = str(j)
                    dt_text = date.replace(date[size - 2:], replacement)
                    tempDaysDictorMonth['day'] = j
                    tempDaysDictorMonth['count'] = BookingDetail.objects.filter(ordered_time__date=dt_text).count()
                    tempDaysorMonth.append(tempDaysDictorMonth)
                    tempDaysDictorMonth = {}
        if is_month ==True:
            d = pd.Timestamp(date)
            num=current_time.month
            m=calendar.month_name[num]
            if int(d.month) == num:
                tempDaysDictorMonth['month'] = m
                tempDaysDictorMonth['count'] = BookingDetail.objects.filter(ordered_time__month=num).count()
                tempDaysorMonth.append(tempDaysDictorMonth)
                tempDaysDictorMonth = {}
            else:
                for j in range(d.day, order_obj['ordered_time'].date().day + 1)[:5]:  #server
                # for j in range(d.month, order_obj['ordered_time__month']+1)[:5]: #local
                        s=calendar.month_name[j]
                        tempDaysDictorMonth['month'] = s
                        tempDaysDictorMonth['count'] = BookingDetail.objects.filter(ordered_time__month=d.month).count()
                        tempDaysorMonth.append(tempDaysDictorMonth)
                        tempDaysDictorMonth = {}
        else:
                print()
        return Response(tempDaysorMonth)
    
class DriverDocumentStatusApi(APIView):
    def get(self,request):
        data = request.data
        if request.query_params:
            doc_obj = DriverDocumentStatus.objects.filter(id=request.query_params['id']).values('id','status_name')
            return Response({'data': doc_obj})
        else:
            doc_obj = DriverDocumentStatus.objects.values('id','status_name')
            return Response({'data':doc_obj})

    def post(self,request):
        data = request.data
        status_name = data['status_name'] 
        # descriptions=data['descriptions']   

        doc_obj = DriverDocumentStatus.objects.create(status_name=data['status_name'])
        return Response({'message':'DriverDocumentStatus added successfully!!'})
    
    def put(self,request,pk):
        data = request.data
        status_name = data['status_name'] 
        # descriptions=data['descriptions']   
        if DriverDocumentStatus.objects.filter(id=pk).exists():
            DriverDocumentStatus.objects.filter(id=pk).update(status_name=status_name)
            return Response({'message': 'DriverDocumentStatus is updated'})
        else:
            return Response({'error':'DriverDocumentStatus id is not found'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        data = request.data
        if DriverDocumentStatus.objects.filter(id=pk).exists():
            DriverDocumentStatus.objects.filter(id=pk).delete()
            return Response({'message': 'DriverDocumentStatus is deleted'})
        else:
            return Response({'error':'DriverDocumentStatus id is not found'},status=status.HTTP_404_NOT_FOUND)


        # current_time = datetime.datetime.now()
        # print("current_time===>", current_time.day)

        # tempDaysorMonth = []
        # tempDaysDictorMonth = {}
        # order_obj = BookingDetail.objects.all().values('ordered_time__day', 'ordered_time__month').last() #local
        
        # order_obj = BookingDetail.objects.all().values('ordered_time').latest('id') #server        
        # if is_days ==True:
        #     d = pd.Timestamp(date)
        #     if int(d.day) == current_time.day:
        #         tempDaysDictorMonth['day'] = d.date()
        #         tempDaysDictorMonth['count'] = BookingDetail.objects.filter(ordered_time__date=date).count()
        #         tempDaysorMonth.append(tempDaysDictorMonth)
        #         tempDaysDictorMonth = {}
        #     else:
        #         size = len(date) 
        #         # for j in range(d.day, order_obj['ordered_time'].date().day + 1)[:5]:  #server
        #         for j in range(d.day, order_obj['ordered_time__day']+ 1)[:5]: #local
        #             replacement = str(j)
        #             dt_text = date.replace(date[size - 2:], replacement)
        #             tempDaysDictorMonth['day'] = d.date()
        #             tempDaysDictorMonth['count'] = BookingDetail.objects.filter(ordered_time__date=dt_text).count()
        #             tempDaysorMonth.append(tempDaysDictorMonth)
        #             tempDaysDictorMonth = {}

        # if is_month ==True:
        #     d = pd.Timestamp(date) 
        #     if int(d.month) == current_time.month:
        #         tempDaysDictorMonth['month'] = d.date()
        #         tempDaysDictorMonth['count'] = BookingDetail.objects.filter(ordered_time__month=d.month).count()
        #         tempDaysorMonth.append(tempDaysDictorMonth)
        #         tempDaysDictorMonth = {}
        #     else:
        #         # for j in range(d.day, order_obj['ordered_time'].date().day + 1)[:5]:  #server
        #         for j in range(d.day, order_obj['ordered_time__month']+ 1)[:5]: #local
        #             tempDaysDictorMonth['month'] = j
        #             tempDaysDictorMonth['count'] = BookingDetail.objects.filter(ordered_time__month=j).count()
        #             tempDaysorMonth.append(tempDaysDictorMonth)
        #             tempDaysDictorMonth = {}
        # else:
        #         print("jhsajhd")
        # return Response(tempDaysorMonth)



def find_vehicle_estimation_cost(data, vehicle_type_id, location_details):

    final_km = {}
    final_min = {}
    vehicle_type= VehicleTypes.objects.get(id=vehicle_type_id)

    
    per_kilm_price = vehicle_type.per_km_price
    per_minute_price = vehicle_type.per_min_price
    offer_price = vehicle_type.offer_price
    min_charge = vehicle_type.min_charge
    free_min = vehicle_type.free_min

    # print("data is printing =>", data)

    if type(data['location_details'])  == dict:

        distance_text = data['location_details']['distance']['text']
        if "km" in distance_text or "m" in distance_text:
            removed_km_text = distance_text.replace('km', '').replace('m', '')

            if "km" in distance_text:
                final_km['final_km'] = float(removed_km_text)
            elif "m" in distance_text:
                m_to_km = float(removed_km_text) / 1000 
                final_km['final_km'] = m_to_km
                

        duration  = data['location_details']['duration']['text']
        if "mins" in duration:
            removed_min_text = duration.replace('mins', '')
            if "mins" in duration:
                final_min['final_min'] = int(removed_min_text)
            if "hour" and "min" in duration:
                pass


        final_km_charage = final_km['final_km'] * float(per_kilm_price)
        
        if free_min is not None:
            remaining_minues = {}
            if final_min['final_min'] <= float(free_min):
                total_charge = final_km_charage + float(min_charge)
                remaining_minues['value'] = 0
            else:
                total_minutes = final_min['final_min'] - float(free_min)
                remaining_minues['value'] = total_minutes
                final_minute_charge = total_minutes * float(per_minute_price)

                total_charge = final_km_charage + final_minute_charge + float(min_charge)

                # total_exact_amount = final_km_charage + final_minute_charge + float(min_charge)

                # print("final km charge=>", final_km_charage,"final_minute_charge=>", final_minute_charge, "min charge=>", min_charge)
                # print("with offer price", total_charge)

                # BookingDetail.objects.filter()

            final_est_cost_output = {
                'message':'calulated output with offer',
                'per_km_price': float(per_kilm_price),
                'per_min_price': float(per_minute_price),
                'free_minutes': float(free_min),
                'total_minutes_of_ride': final_min['final_min'],
                'total_km_of_ride': final_km['final_km'],
                'remaining_miutes': remaining_minues['value'],
                'base_fee': float(min_charge),
                'total_fare_amount': round(total_charge,2),
                'final_km_charge': final_km_charage,
            }

            return final_est_cost_output
        else:
            final_minute_charge = final_min['final_min'] * float(per_minute_price)
            total_charge = final_km_charage + final_minute_charge + float(min_charge) 
            # print("without", total_charge)

            final_est_cost_output = {
                'message':'calulated output without offer',
                'per_km_price': float(per_kilm_price),
                'base_fee': float(min_charge),
                'per_min_price': float(per_minute_price),
                'total_fare_amount': round(total_charge,2),
                'total_minutes_of_ride': final_min['final_min'],
                'total_km_of_ride': final_km['final_km'],
                'final_km_charge': final_km_charage,
                }

            return final_est_cost_output

    else:

        final_km = []
        final_min = []

        for i in location_details:

            # print("i value==>", i)

            # print("printing i value==>>", i['distance']['text'])

            distance_text = i['distance']['text']

            if "km" in distance_text or "m" in distance_text:
                removed_km_text = distance_text.replace('km', '').replace('m', '')

                # print("removed ==>",removed_km_text)

                if "km" in distance_text:
                    final_km.append(float(removed_km_text))
                elif "m" in distance_text:
                    m_to_km = float(removed_km_text) / 1000 
                    final_km.append(float(m_to_km))
                    

            duration  = i['duration']['text']
            if "mins" in duration:
                removed_min_text = duration.replace('mins', '')
                if "mins" in duration:
                    final_min.append(float(removed_min_text))
                if "hour" and "min" in duration:
                    pass

        final_km_charage = abs(sum(final_km)) * float(per_kilm_price)
        # final_minute_charge = abs(sum(final_min)) * float(per_minute_price)

        if free_min is not None:
            remaining_minues = {}
            if abs(sum(final_min)) <= float(free_min):
                total_charge = final_km_charage + float(min_charge)
                remaining_minues['value'] = 0
            
            else:
                total_minutes = abs(sum(final_min)) - float(free_min)
                remaining_minues['value'] = total_minutes
                final_minute_charge = total_minutes * float(per_minute_price)
                
                total_charge = final_km_charage + final_minute_charge + float(min_charge)
                # print("with offer price", total_charge)

            final_est_cost_op = {
                'message':'calulated output with offer',
                'per_km_price': float(per_kilm_price),
                'per_min_price': float(per_minute_price),
                'base_fee': float(min_charge),
                'total_fare_amount': total_charge,

                'free_minutes': float(free_min),
                'total_minutes_of_ride': abs(sum(final_min)),
                'total_km_of_ride': abs(sum(final_km)),
                'remaining_miutes': remaining_minues['value'],
                'final_km_charge': final_km_charage,
                }
            return final_est_cost_op
        else:
            final_minute_charge = abs(sum(final_min)) * float(per_minute_price)
            total_charge = final_km_charage + final_minute_charge + float(min_charge) 
            # print("without", total_charge)

            final_est_cost_op = {
                'message':'calulated output without offer', 
                'per_km_price': float(per_kilm_price),
                'per_min_price': float(per_minute_price),
                'total_fare_amount': total_charge,
                'total_minutes_of_ride': abs(sum(final_min)),
                'base_fee': float(min_charge),
                'total_km_of_ride': abs(sum(final_km)),
                'final_km_charge': final_km_charage, 
                }
            return final_est_cost_op


class vehicle_estimation_costApi(APIView):
    def post(self, request):
        data=request.data

        vehicle_type_id=data.get('vehicle_type_id')
        location_details=data.get('location_details')

        op = find_vehicle_estimation_cost(data, vehicle_type_id ,location_details)
        # print('op[====]',op)
        return Response(op)


        # final_km = {}
        # final_min = {}
        # vehicle_type= VehicleTypes.objects.get(id=vehicle_type_id)

        # per_kilm_price = vehicle_type.per_km_price
        # per_minute_price = vehicle_type.per_min_price
        # offer_price = vehicle_type.offer_price
        # min_charge = vehicle_type.min_charge
        # free_min = vehicle_type.free_min

        # if type(location_details)  == dict:

        #     distance_text = data['location_details']['distance']['text']
        #     if "km" in distance_text or "m" in distance_text:
        #         removed_km_text = distance_text.replace('km', '').replace('m', '')

        #         if "km" in distance_text:
        #             final_km['final_km'] = float(removed_km_text)
        #         elif "m" in distance_text:
        #             m_to_km = float(removed_km_text) / 1000 
        #             final_km['final_km'] = m_to_km
                    

        #     duration  = data['location_details']['duration']['text']
        #     if "mins" in duration:
        #         removed_min_text = duration.replace('mins', '')
        #         if "mins" in duration:
        #             final_min['final_min'] = int(removed_min_text)
        #         if "hour" and "min" in duration:
        #             pass


        #     final_km_charage = final_km['final_km'] * float(per_kilm_price)
            
        #     if free_min is not None:
        #         remaining_minues = {}
        #         if final_min['final_min'] <= float(free_min):
        #             total_charge = final_km_charage + float(min_charge)
        #             remaining_minues['value'] = 0
        #         else:
        #             total_minutes = final_min['final_min'] - float(free_min)
        #             remaining_minues['value'] = total_minutes
        #             final_minute_charge = total_minutes * float(per_minute_price)

        #             total_charge = final_km_charage + final_minute_charge + float(min_charge)
        #             print("final km charge=>", final_km_charage,"final_minute_charge=>", final_minute_charge, "min charge=>", min_charge)
        #             print("with offer price", total_charge)

        #             # BookingDetail.objects.filter()

        #         return Response({
        #             'message':'calulated output with offer',
        #             'per_km_price': float(per_kilm_price),
        #             'per_min_price': float(per_minute_price),
        #             'free_minutes': float(free_min),
        #             'total_minutes_of_ride': final_min['final_min'],
        #             'total_km_of_ride': final_km['final_km'],
        #             'remaining_miutes': remaining_minues['value'],
        #             'base_fee': float(min_charge),
        #             'total_fare_amount': total_charge,
        #             })
        #     else:
        #         final_minute_charge = final_min['final_min'] * float(per_minute_price)
        #         total_charge = final_km_charage + final_minute_charge + float(min_charge) 
        #         print("without", total_charge)

        #         return Response({
        #             'message':'calulated output without offer',
        #             'per_km_price': float(per_kilm_price),
        #             'base_fee': float(min_charge),
        #             'per_min_price': float(per_minute_price),
        #             'total_fare_amount': total_charge,
        #             'total_minutes_of_ride': final_min['final_min'],
        #             'total_km_of_ride': final_km['final_km'],
        #             })

        # else:
        #     print()

        #     location_details = data['location_details']

        #     final_km = []
        #     final_min = []

        #     for i in location_details:

        #         distance_text = i['distance']['text']

        #         if "km" in distance_text or "m" in distance_text:
        #             removed_km_text = distance_text.replace('km', '').replace('m', '')

        #             print("removed ==>",removed_km_text)

        #             if "km" in distance_text:
        #                 final_km.append(float(removed_km_text))
        #             elif "m" in distance_text:
        #                 m_to_km = float(removed_km_text) / 1000 
        #                 final_km.append(float(m_to_km))
                        

        #         duration  = i['duration']['text']
        #         if "mins" in duration:
        #             removed_min_text = duration.replace('mins', '')
        #             if "mins" in duration:
        #                 final_min.append(float(removed_min_text))
        #             if "hour" and "min" in duration:
        #                 pass

        #     final_km_charage = abs(sum(final_km)) * float(per_kilm_price)
        #     # final_minute_charge = abs(sum(final_min)) * float(per_minute_price)

        #     if free_min is not None:
        #         remaining_minues = {}
        #         if abs(sum(final_min)) <= float(free_min):
        #             total_charge = final_km_charage + float(min_charge)
        #             remaining_minues['value'] = 0
                
        #         else:
        #             total_minutes = abs(sum(final_min)) - float(free_min)
        #             remaining_minues['value'] = total_minutes
        #             final_minute_charge = total_minutes * float(per_minute_price)
                    
        #             total_charge = final_km_charage + final_minute_charge + float(min_charge)
        #             # print("with offer price", total_charge)

        #         return Response({
        #             'message':'calulated output with offer',
        #             'per_km_price': float(per_kilm_price),
        #             'per_min_price': float(per_minute_price),
        #             'base_fee': float(min_charge),
        #             'total_fare_amount': total_charge,

        #             'free_minutes': float(free_min),
        #             'total_minutes_of_ride': abs(sum(final_min)),
        #             'total_km_of_ride': abs(sum(final_km)),
        #             'remaining_miutes': remaining_minues['value']
        #             })
        #     else:
        #         final_minute_charge = abs(sum(final_min)) * float(per_minute_price)
        #         total_charge = final_km_charage + final_minute_charge + float(min_charge) 
        #         print("without", total_charge)

        #         return Response({
        #             'message':'calulated output without offer', 
        #             'per_km_price': float(per_kilm_price),
        #             'per_min_price': float(per_minute_price),
        #             'total_fare_amount': total_charge,
        #             'total_minutes_of_ride': abs(sum(final_min)),
        #             'base_fee': float(min_charge),
        #             'total_km_of_ride': abs(sum(final_km)),
        #             })
                    


            


class accept_statusApi(APIView):
    def get(self,request):
        status_name = request.query_params.get('status_name')
        order_accepted_time=request.query_params.get('order_accepted_time')
        # print('ppppppppppp===',order_accepted_time)
        if status_name:
            if order_accepted_time:
                count = 0
                matching_orders = []
                order_accepted_time_count = BookingDetail.objects.filter(
                    status__status_name=status_name
                ).values('id','order__user_id__first_name','order__user_id__mobile_number','status__colour','status__status_name','driver__first_name','driver__mobile_number',
                    'ordered_time','last_update_timestamp','order_id','order__vehicle_number','ordered_time','total_amount_without_actual_time_taken','scheduledorder__scheduled_date_and_time','order__total_estimated_cost','order_accepted_time')
                for i in order_accepted_time_count:
                    if i['order_accepted_time'] and str(i['order_accepted_time'].date()) == order_accepted_time:
                        count += 1
                        matching_orders.append(i)
                return Response({'order_accepted_time_count': count, 'matching_orders': matching_orders})
            else:
                order_accepted_time_count = BookingDetail.objects.filter(
                    status__status_name=status_name
                ).values('id','order__user_id__first_name','order__user_id__mobile_number','status__colour','status__status_name','driver__first_name','driver__mobile_number',
                    'ordered_time','last_update_timestamp','order_id','order__vehicle_number','ordered_time','total_amount_without_actual_time_taken','scheduledorder__scheduled_date_and_time','order__total_estimated_cost','order_accepted_time')
                accept_orders_count = order_accepted_time_count.count()
                return Response({'accept_orders_count': accept_orders_count, 'matching_orders': list(order_accepted_time_count)})
        return Response({'message': 'Invalid parameters'})



class Decline_statusApi(APIView):
    def get(self,request):
        status_name = request.query_params.get('status_name')
        date=request.query_params.get('date')
        declined_time=request.query_params.get('declined_time')

        if status_name:
            if declined_time:
                count = 0
                matching_orders = []
                order_declined_time_count = BookingDetail.objects.filter(
                    status__status_name=status_name
                ).values('id','order__user_id__first_name','order__user_id__mobile_number','status__colour','status__status_name','driver__first_name','driver__mobile_number',
                    'ordered_time','last_update_timestamp','order_id','order__vehicle_number','ordered_time','total_amount_without_actual_time_taken','scheduledorder__scheduled_date_and_time','order__total_estimated_cost','order_accepted_time', 'declined_time')
                for i in order_declined_time_count:
                    if 'declined_time' in i and i['declined_time'] and str(i['declined_time'].date()) == declined_time:
                        count += 1
                        matching_orders.append(i)
                return Response({'decline_orders_count': count, 'matching_orders': matching_orders})
            else:
                order_declined_time_count = BookingDetail.objects.filter(
                    status__status_name=status_name
                ).values('id','order__user_id__first_name','order__user_id__mobile_number','status__colour','status__status_name','driver__first_name','driver__mobile_number',
                    'ordered_time','last_update_timestamp','order_id','order__vehicle_number','ordered_time','total_amount_without_actual_time_taken','scheduledorder__scheduled_date_and_time','order__total_estimated_cost','order_accepted_time')
                accept_orders_count = order_declined_time_count.count()
                return Response({'decline_orders_count': accept_orders_count, 'matching_orders': list(order_declined_time_count)})
        return Response({'message': 'Invalid parameters'})


class Pending_statusApi(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        status_name = request.query_params.get('status_name')
        # print('status_name==============',status_name)
        if status_name and date:
            count = 0
            matching_orders = []
            pending_order_status_count = BookingDetail.objects.filter(status__status_name=status_name).values('id','order__user_id__first_name','order__user_id__mobile_number','status__colour','status__status_name','driver__first_name','driver__mobile_number','ordered_time','last_update_timestamp','order_id','order__vehicle_number','total_amount_without_actual_time_taken','scheduledorder__scheduled_date_and_time','order__total_estimated_cost')
            for booking_detail in pending_order_status_count:
                if booking_detail.get('ordered_time') and str(booking_detail.get('ordered_time').date()) == date:
                    if booking_detail.get('canceled_time') is None and booking_detail.get('declined_time') is None and booking_detail.get('trip_ended_time') is None:
                        count += 1
                        matching_orders.append(booking_detail)
            return Response({'pending_order_status_count': count, 'matching_orders': matching_orders})
        else:
            pending_order_status_count = BookingDetail.objects.filter(status__status_name=status_name).values('id','order__user_id__first_name','order__user_id__mobile_number','status__colour','status__status_name','driver__first_name','driver__mobile_number','ordered_time','last_update_timestamp','order_id','order__vehicle_number','total_amount_without_actual_time_taken','scheduledorder__scheduled_date_and_time','order__total_estimated_cost')
            pending_orders_count = pending_order_status_count.count()
            return Response({'pending_orders_count': pending_orders_count})
  
class RemarksApi(APIView):
    def get(self,request):
        id = request.query_params.get('id')
        driver_id = request.query_params.get('driver_id')
        if id:
            remark_obj = Remarks.objects.filter(id = id).values('id','driver_id','document_status__id','text','document_status__status_name')
            return Response({'data':remark_obj})
        
        if driver_id:
            remark = Remarks.objects.filter(driver_id=driver_id).values('id','driver_id','document_status__id','text','document_status__status_name')
            return Response({'data':remark})
        else:
            obj = Remarks.objects.all().values('id','driver_id','document_status__id','text','document_status__status_name')
            return Response({'data':obj})

    def post(self,request):
        data = request.data
        driver_id = data.get('driver_id') 
        document_id=data.get('document_id') 
        text=data['text']
        if Driver.objects.filter(id=data['driver_id']).exists():
            driver=Driver.objects.get(id=data['driver_id'])
            # print('=====<><>AAAAAAa',driver)
            remark_obj= Remarks.objects.create(driver_id_id=driver_id,text=text,document_status_id=document_id)
            return Response({'data':'Remarks Successfully Added!!'})
        else:
            return Response({'error':'driver id not found!!'},status=status.HTTP_406_NOT_ACCEPTABLE)

    def put(self,request,pk):
        data = request.data
        driver_id = data.get('driver_id') 
        document_id=data.get('document_id')
        text=data.get('text')
        if Remarks.objects.filter(id=pk).exists():
            Remarks.objects.filter(id=pk).update(document_status_id=document_id,text=text,driver_id_id=driver_id)
            return Response({'message': 'Remarks is updated'})
        else:
            return Response({'error':'Remarks id is not found'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        data = request.data
        if Remarks.objects.filter(id=pk).exists():
            Remarks.objects.filter(id=pk).delete()
            return Response({'message': 'Remarks is deleted'})
        else:
            return Response({'error':'Remarks id is not found'},status=status.HTTP_404_NOT_FOUND)

import pytz
import datetime
datetime.datetime.now()
from datetime import datetime, timedelta
class FilterCountApi(APIView):
    def get(self,request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        status_id = request.query_params.get('status_id')
        ordered_time = request.query_params.get('ordered_time')
        year = request.query_params.get('year')
        current_date = datetime.datetime.now().date()
        last_10_days = [current_date - datetime.timedelta(days=x) for x in range(10)]
        bookings = BookingDetail.objects.all().select_related('order', 'status').values(
            'id', 'order__user_id', 'order_id', 'driver_id', 'status__id', 'status__status_name', 'ordered_time'
        )
        color_dict = {
            'InProgress': 'rgb(234,227,100)',
            'Accepted': 'rgb(116,231,170)',
            'Declined': 'Orange',
            'Trip Ended': 'Green',
            'Cancelled': 'rgb(237,74,74)',
            'PickedUp': 'Pink',
            'Request-cancel-ride': 'Gray',
            'Accept-cancel-ride': 'Purpule',
            'Decline-cancel-ride': 'Brown',    
        }


        # if year and start_date and end_date:
        #     start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        #     end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        #     response_data = []
        #     if status_id is not None:
        #         status_id_list = re.findall(r'\d+', status_id)
        #         status_id_list = [int(num) for num in status_id_list][:10]  # limit to 10 status ids
        #         for status_id in status_id_list:
        #             order_counts = []
        #             for day in range((end_date - start_date).days + 1):
        #                 date = start_date + datetime.timedelta(days=day)
        #                 next_date = date + datetime.timedelta(days=1)
        #                 count = bookings.filter(
        #                     ordered_time__gte=date, ordered_time__lt=next_date, status__id=status_id
        #                 ).count()
        #                 order_counts.append({'date': date, 'count': count})
        #             status_record = Status.objects.filter(id=status_id).first()
        #             if status_record:
        #                 status_name = status_record.status_name
        #                 color = color_dict.get(status_name, 'black') # lookup color for status
        #             else:
        #                 status_name = f'Status {status_id}'
        #                 color = 'black'
        #             response_data.append({
        #                 'status_name': status_name,
        #                 'color': color,
        #                 'order_counts': order_counts
        #             })
        #     else:
        #         order_counts = []
        #         for day in range((end_date - start_date).days + 1):
        #             date = start_date + datetime.timedelta(days=day)
        #             next_date = date + datetime.timedelta(days=1)
        #             count = bookings.filter(
        #                 ordered_time__gte=date, ordered_time__lt=next_date
        #             ).count()
        #             order_counts.append({'date': date, 'count': count})
        #         response_data.append({
        #             'status_name': 'All',
        #             'color': 'black',
        #             'order_counts': order_counts
        #         })

        #     return Response(response_data)


        if year and start_date and end_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            response_data = []
            if status_id is not None:
                status_id_list = re.findall(r'\d+', status_id)
                status_id_list = [int(num) for num in status_id_list][:10]  # limit to 10 status ids
                for status_id in status_id_list:
                    order_counts = []
                    for day in range((end_date - start_date).days + 1):
                        date = start_date + datetime.timedelta(days=day)
                        next_date = date + datetime.timedelta(days=1)
                        bookings_filter = bookings.filter(
                            ordered_time__gte=date, ordered_time__lt=next_date, status__id=status_id, ordered_time__year=year
                        )
                        count = bookings_filter.count()
                        # print(f'status_id={status_id}, date={date}, count={count}, filter={bookings_filter.query}')
                        order_counts.append({'date': date, 'count': count})
                    status_record = Status.objects.filter(id=status_id).first()
                    if status_record:
                        status_name = status_record.status_name
                        color = color_dict.get(status_name, 'black') 
                    else:
                        status_name = f'Status {status_id}'
                        color = 'black'
                    response_data.append({
                        'status_name': status_name,
                        'color': color,
                        'order_counts': order_counts
                    })
            else:
                order_counts = []
                for day in range((end_date - start_date).days + 1):
                    date = start_date + datetime.timedelta(days=day)
                    next_date = date + datetime.timedelta(days=1)
                    bookings_filter = bookings.filter(
                        ordered_time__gte=date, ordered_time__lt=next_date, ordered_time__year=year
                    )
                    count = bookings_filter.count()
                    # print(f'date={date}, count={count}, filter={bookings_filter.query}')
                    order_counts.append({'date': date, 'count': count})
                response_data.append({
                    'status_name': 'All',
                    'color': 'black',
                    'order_counts': order_counts
                })

            return Response(response_data)

        if year and status_id:
            status_id_list = re.findall(r'\d+', status_id)
            status_id_list = [int(num) for num in status_id_list]
            response_data = []
            for status_id in status_id_list:
                status_record = Status.objects.get(id=status_id)
                status_name = status_record.status_name
                color = color_dict.get(status_name, 'default_color')
                order_counts = {}
                for month in range(1, 13):
                    days_in_month = calendar.monthrange(int(year), month)[1]
                    for day in range(1, days_in_month + 1):
                        ordered_date_str = f"{year}-{month:02}-{day:02}"
                        ordered_date = datetime.datetime.strptime(ordered_date_str, '%Y-%m-%d').date()
                        count = 0
                        for booking in bookings.filter(status_id=status_id):
                            if booking['ordered_time'].date() == ordered_date:
                                count += 1
                        order_counts[ordered_date.strftime('%Y-%m-%d')] = count

                response_data.append({
                    'status_name': status_name,
                    'color': color,
                    'order_counts': [{'date': ordered_date.strftime('%Y-%m-%d'), 'count': order_counts.get(ordered_date.strftime('%Y-%m-%d'), 0)} for ordered_date in pd.date_range(f'{year}-01-01', f'{year}-12-31').date]
                })
            return Response(response_data)
        return Response([])
    

        # if year and status_id:
        #     status_id_list = re.findall(r'\d+', status_id)
        #     status_id_list = [int(num) for num in status_id_list]
        #     response_data = []
        #     for status_id in status_id_list:
        #         status_record = Status.objects.get(id=status_id)
        #         status_name = status_record.status_name
        #         color = color_dict.get(status_name, 'default_color')
        #         order_counts = {}
        #         for month in range(1, 13):
        #             days_in_month = calendar.monthrange(int(year), month)[1]
        #             for day in range(1, days_in_month + 1):
        #                 ordered_date_str = f"{year}-{month:02}-{day:02}"
        #                 ordered_date = datetime.datetime.strptime(ordered_date_str, '%Y-%m-%d').date()
        #                 count = 0
        #                 for booking in bookings.filter(status_id=status_id):
        #                     if booking.order and booking.order.ordered_time.date() == ordered_date:
        #                         count += 1
        #                 order_counts[ordered_date.strftime('%Y-%m-%d')] = count

        #         response_data.append({
        #             'status_name': status_name,
        #             'color': color,
        #             'order_counts': [{'date': ordered_date.strftime('%Y-%m-%d'), 'count': order_counts.get(ordered_date.strftime('%Y-%m-%d'), 0)} for ordered_date in pd.date_range(f'{year}-01-01', f'{year}-12-31').date]
        #         })
        #     return Response(response_data)
        # return Response([])
            






        # if year and status_id:  
        #     status_id_list = re.findall(r'\d+', status_id)
        #     status_id_list = [int(num) for num in status_id_list]
        #     response_data = []
        #     for status_id in status_id_list:
        #         status_record = Status.objects.get(id=status_id)
        #         status_name = status_record.status_name
        #         color = color_dict.get(status_name)
        #         order_counts = []
        #         for day in last_10_days:
        #             start_time = datetime.datetime.combine(day, datetime.time.min)
        #             end_time = datetime.datetime.combine(day, datetime.time.max)
        #             count = bookings.filter(
        #                 ordered_time__range=(start_time, end_time), status_id=status_id, ordered_time__year=year
        #             ).count()
        #             order_counts.append({'date': day, 'count': count})

        #         response_data.append({
        #             'status_name': status_name,
        #             'color': color,
        #             'order_counts': order_counts[::-1]
        #         })
        #     return Response(response_data)
        # return Response([])




        
        # data = request.data
        # status_id = request.query_params.get('status_id')
        # start_date = request.query_params.get('start_date')
        # end_date = request.query_params.get('end_date')
        # ordered_time = request.query_params.get('ordered_time')
        # Book_obj = BookingDetail.objects.all().values('id', 'order__user_id', 'order_id', 'driver_id','ordered_time')
        # if status_id and start_date and end_date:
        #     status_id_list = re.findall(r'\d+', status_id)
        #     status_id_list = [int(num) for num in status_id_list]
        #     end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        #     end_date = end_date + datetime.timedelta(days=1)
        #     msg_obj = BookingDetail.objects.filter(Q(ordered_time__gte=start_date) & Q(ordered_time__lte=end_date) & Q(status__id__in=status_id_list)).values('id','order__user_id', 'order_id', 'driver_id', 'status__status_name','ordered_time')
        #     count = msg_obj.count()
        #     orders_by_date = {}
        #     datewise_counts = []
        #     for order in msg_obj:
        #         date = order['ordered_time'].date()
        #         orders_by_date[date] = orders_by_date.get(date, 0) + 1
        #         status = order['status__status_name']
        #         status_count = {status: orders_by_date[date]}
        #         datewise_count = {'date': date.isoformat(), 'count': orders_by_date[date], 'statuswise_counts': status_count}
        #         datewise_counts.append(datewise_count)
        #     return Response({'order_detail': msg_obj, 'count': count, 'datewise_counts': datewise_counts})

        # if status_id:
        #     status_id_list = re.findall(r'\d+', status_id)
        #     status_id_list = [int(num) for num in status_id_list]
        #     msg_obj = BookingDetail.objects.filter(Q(status__id__in=status_id_list)).values('id','order__user_id', 'order_id', 'status__status_name','ordered_time')
        #     count = msg_obj.count()
        #     orders_by_date = {}
        #     datewise_counts = []
        #     for order in msg_obj:
        #         date = order['ordered_time'].date()
        #         orders_by_date[date] = orders_by_date.get(date, 0) + 1
        #         status = order['status__status_name']
        #         status_count = {status: orders_by_date[date]}
        #         datewise_count = {'date': date.isoformat(), 'count': orders_by_date[date], 'statuswise_counts': status_count}
        #         datewise_counts.append(datewise_count)
        #     return Response({'order_detail': msg_obj, 'count': count, 'datewise_counts': datewise_counts})

        # msg_obj = BookingDetail.objects.all().values('id','order__user_id', 'order_id', 'driver_id', 'status__status_name','ordered_time')
        # count = msg_obj.count()
        # orders_by_date = {}
        # datewise_counts = []
        # for order in msg_obj:
        #     date = order['ordered_time'].date()
        #     orders_by_date[date] = orders_by_date.get(date, 0) + 1
        #     status = order['status__status_name']
        #     status_count = {status: orders_by_date[date]}
        #     datewise_count = {'date': date.isoformat(), 'count': orders_by_date[date], 'statuswise_counts': status_count}
        #     datewise_counts.append(datewise_count)
        # return Response({'order_detail': msg_obj, 'count': count, 'datewise_counts': datewise_counts, 'statuswise_counts':statuswise_counts})


        # if status_id and start_date and end_date:
        #     status_id_list = re.findall(r'\d+', status_id)
        #     status_id_list = [int(num) for num in status_id_list]
        #     end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        #     end_date = end_date + datetime.timedelta(days=1)
        #     msg_obj = BookingDetail.objects.filter(Q(ordered_time__gte=start_date) & Q(ordered_time__lte=end_date) & Q(status__id__in=status_id_list)).values('id','order__user_id', 'order_id', 'driver_id', 'status','order__vehicle_number', 'total_amount','order__user_id__first_name', 'order__user_id__mobile_number','status__status_name', 'order__otp','driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp', 'driver__first_name','status__colour','driver__mobile_number', 'ordered_time', 'is_scheduled','scheduledorder__scheduled_date_and_time')
        #     count = msg_obj.count()
        #     orders_by_date = {}
        #     for order in msg_obj:
        #         date = order['ordered_time'].date()
        #         orders_by_date[date] = orders_by_date.get(date, 0) + 1
        #     datewise_counts = [{'date': date.isoformat(), 'count': count} for date, count in orders_by_date.items()]
        #     return Response({'order_detail': msg_obj, 'count': count, 'datewise_counts': datewise_counts})

        # if status_id:
        #     status_id_list = re.findall(r'\d+', status_id)
        #     status_id_list = [int(num) for num in status_id_list]
        #     msg_obj = BookingDetail.objects.filter(Q(status__id__in=status_id_list)).values('id','order__user_id', 'order_id', 'driver_id', 'status','order__vehicle_number', 'total_amount','order__user_id__first_name', 'order__user_id__mobile_number','status__status_name', 'order__otp','driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp', 'driver__first_name','status__colour','driver__mobile_number', 'ordered_time', 'is_scheduled','scheduledorder__scheduled_date_and_time')
        #     count = msg_obj.count()
        #     orders_by_date = {}
        #     for order in msg_obj:
        #         date = order['ordered_time'].date()
        #         orders_by_date[date] = orders_by_date.get(date, 0) + 1
        #     datewise_counts = [{'date': date.isoformat(), 'count': count} for date, count in orders_by_date.items()]
        #     return Response({'order_detail': msg_obj, 'count': count, 'datewise_counts': datewise_counts})

        # msg_obj = BookingDetail.objects.all().values('id','order__user_id', 'order_id', 'driver_id', 'status','order__vehicle_number', 'total_amount','order__user_id__first_name', 'order__user_id__mobile_number','status__status_name', 'order__otp','driver__vehicle__vehicle_name', 'order__total_estimated_cost','last_update_timestamp', 'driver__first_name','status__colour','driver__mobile_number', 'ordered_time', 'is_scheduled','scheduledorder__scheduled_date_and_time')
        # count = msg_obj.count()
        # orders_by_date = {}
        # for order in msg_obj:
        #     date = order['ordered_time'].date()
        #     orders_by_date[date] = orders_by_date.get(date, 0) + 1
        # datewise_counts = [{'date': date.isoformat(), 'count': count} for date, count in orders_by_date.items()]
        # return Response({'order_detail': msg_obj, 'count': count, 'datewise_counts': datewise_counts})


        # year = request.query_params.get('year')
        # print("year", year, type(year))
        # month = request.query_params.get('month')
        # print("month",month)
        # week = request.query_params.get('week')
        # print("week",week)
        # day=request.query_params.get('day')
        # print("day")
        # status_id=request.query_params.get('status_id')
        # day_arr=[]
        # month_arr=[]
        # week_arr=[]
        # status=[]
        # dayList = []

        # if year and month and week and status_id:
        #     start_date = datetime.datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d").date()
        #     print('start___________',start_date)
        #     weekday = start_date.weekday()
        #     if weekday > 0:
        #         start_date = start_date - datetime.timedelta(days=weekday)
        #         print('------------',start_date)
        #     start_date += datetime.timedelta(weeks=int(week) - 1)
        #     print('dddddddd',start_date)
        #     end_date = start_date + datetime.timedelta(days=6)

        #     bookings = BookingDetail.objects.filter(
        #         ordered_time__gte=start_date,
        #         ordered_time__lte=end_date,
        #         status__id=status_id
        #     ).values('ordered_time', 'status_id')

        #     for i in range((end_date - start_date).days + 1):
        #         date = start_date + datetime.timedelta(days=i)
        #         count = 0
        #         for booking in bookings:
        #             if booking['ordered_time'].date() == date and booking['status_id'] == int(status_id):
        #                 count += 1
        #         dayList.append({'day': date.strftime('%A'), 'order_count': count})

        #     return Response(dayList)

        # if(year and month):
        #     tempList = []
        #     tempDayList = []
        #     day_wise_order_count=BookingDetail.objects.filter(ordered_time__year=int(year),status_id=status_id).values('ordered_time')
            
        #     for k in day_wise_order_count:
        #         if k['ordered_time'].month == int(month):
        #             print('iiiiiiiiiiiiiiiiiiii',k['ordered_time'].month)
        #             tempDayList.append(int(k['ordered_time'].day))
        #             tempList.append({k['ordered_time'].month : k['ordered_time'].day})

        #     finalDict = {}
        #     finalArr = []

        #     last_date=calendar.monthrange(int(year), int(month))[1]
        #     for i in range(1,last_date+1):
        #         finalDict['day'] = i
        #         finalDict['order_count'] = tempDayList.count(i)
        #         finalDict['status_id']=status_id
        #         finalArr.append(finalDict)
        #         finalDict = {}
                
        #     week=[]
        #     year = int(year)
        #     month = int(month)

        #     num_weeks = calendar.monthcalendar(year, month)
        #     print('num_weeks==============',num_weeks)
        #     numweeks = len([week for week in num_weeks if week[calendar.SUNDAY] != 0])
        #     print('numweeks========<<<<<<',numweeks)
        #     week.append(numweeks)

        #     return Response({'data':finalArr,'number_of_weeks':[numweeks]}) 
                
        # if(year):
        #     tempList = []
        #     month_wise_order_count=BookingDetail.objects.filter(ordered_time__year=int(year),status_id=status_id).values('ordered_time')
        #     for i in month_wise_order_count:
        #         print(i['ordered_time'].month)
        #         tempList.append(i['ordered_time'].month)
        #     for i in range(1,13):
        #         month_arr.append({
        #             'month':calendar.month_name[i],
        #             'order_count':tempList.count(i),
        #             'status_id':status_id
        #         })        
        #     return Response(month_arr)


class DriverDocumentExpiryvalidityApi(APIView):
    def get(self,request):
        data = request.data
        id = request.query_params.get('id')
        due_date = request.query_params.get('due_date')
        description = request.query_params.get('description')
        label = request.query_params.get('label')
        if id:
            val_obj = DriverDocumentExpiryvalidity.objects.filter(id = id).values()
            return Response({'data':val_obj})
        else:
            val_obj = DriverDocumentExpiryvalidity.objects.all().values()
            return Response({'data':val_obj})

    def post(self, request):
        data = request.data
        due_date = data['due_date']
        labels = data['label']
        description = data['description']

        for label in labels:
            try:
                val_obj = DriverDocumentExpiryvalidity.objects.get(label=label)
                # Update the existing entry
                val_obj.due_date = due_date
                val_obj.description = description
                val_obj.save()
            except DriverDocumentExpiryvalidity.DoesNotExist:
                # Create a new entry
                val_obj = DriverDocumentExpiryvalidity.objects.create(
                    due_date=due_date,
                    label=label,
                    description=description
                )

        return Response({'data': 'Validity days successfully added!!'})

    def put(self,request,pk):
        data = request.data
        due_date=data.get('due_date')
        label=data.get('label')
        description=data.get('description')
        if DriverDocumentExpiryvalidity.objects.filter(id=pk).exists():
            DriverDocumentExpiryvalidity.objects.filter(id=pk).update(due_date=due_date,label=label,description=description)
            return Response({'message': 'validitydays is updated'})
        else:
            return Response({'error':'DriverDocumentExpiryvalidity id is not found'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        data = request.data
        if DriverDocumentExpiryvalidity.objects.filter(id=pk).exists():
            DriverDocumentExpiryvalidity.objects.filter(id=pk).delete()
            return Response({'message': 'validitydays is deleted'})
        else:
            return Response({'error':'DriverDocumentExpiryvalidity id is not found'},status=status.HTTP_404_NOT_FOUND)

import pandas as pd

class Delete_vehicle_imageApi(APIView):
    def delete(self, request, vehicle_type_id):
        img_index_id = request.query_params.get('img_index_id')  
        des_index_id = request.query_params.get('des_index_id')    
        if(img_index_id):    
            val_obj=VehicleTypes.objects.get(id=vehicle_type_id)
            img_list=val_obj.vehicle_type_sub_images
            removed_value = img_list.pop(int(img_index_id))
            update_vehicle_type_sub_img= VehicleTypes.objects.filter(id=vehicle_type_id).update(vehicle_type_sub_images=img_list)      
            return Response({'data':'image deleted sucessfully!!!'})
        else:
            val_obj=VehicleTypes.objects.get(id=vehicle_type_id)
            des_list=val_obj.vehicle_description
            # print('ggggggg=====>>>>',des_list)
            removed_value = des_list[0]['description'].pop(int(des_index_id))
            # print('fgffffffffffffff=====>>',removed_value)
            # print('ggggg',des_list[0]['description'])
            update_vehicle_type_sub_img= VehicleTypes.objects.filter(id=vehicle_type_id).update(vehicle_description=des_list)      
            return Response({'data':'description deleted sucessfully!!!'})
            
from datetime import datetime, date  

class dateOrderDetailsApi(APIView):
    def post(self,request):
        data = request.query_params
        status_id = data.getlist('status_id')
        start_date = data['start_date']
        end_date = data['end_date']
        ordered_times = data.getlist('ordered_time')
        end_date_plus_one = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        order_status_count = BookingDetail.objects.filter(
            ordered_time__range=(start_date, end_date_plus_one),
            status_id__in=status_id
        ).values(
            'id',
            'order__user_id__first_name',
            'order__user_id__mobile_number',
            'status__colour',
            'status__status_name',
            'driver__first_name',
            'driver__mobile_number',
            'ordered_time',
            'last_update_timestamp',
            'order_id',
            'order__vehicle_number'
        )
        order_status_count_reversed = reversed(order_status_count)
        # print('order_status_count=======>>>>>>', order_status_count)

        return Response(order_status_count_reversed)

        # data=request.data
        # status_id=data['status_id']
        # start_date=data['start_date']
        # end_date=data['end_date']
        # ordered_times=data.get('ordered_time')
        # end_date_plus_one = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
        # order_status_count = BookingDetail.objects.filter(
        #     ordered_time__range=(start_date, end_date_plus_one),
        #     status_id__in=status_id
        # ).values(
        #     'id',
        #     'order__user_id__first_name',
        #     'order__user_id__mobile_number',
        #     'status__colour',
        #     'status__status_name',
        #     'driver__first_name',
        #     'driver__mobile_number',
        #     'ordered_time',
        #     'last_update_timestamp',
        #     'order_id',
        #     'order__vehicle_number'
        # )
        # reverse_obj=reversed(order_status_count)
        # print('order_status_count=======>>>>>>',order_status_count)

        # return Response(reverse_obj)

import smtplib
class SendmessageApi(APIView):
    def get(self,request):
        # data = request.data
        # id = request.query_params.get('id')
        # driver_id=request.query_params.get('driver_id')
        # default=request.query_params.get('default')
        # if driver_id:
        #     tempList=[]
        #     msg_obj = Sendmessage.objects.filter(driver__user__id=driver_id).values('id','def_message','def_message__default_message','driver')
        #     tempList.append(msg_obj)
        #     # print('dsahj',tempList)
        #     return Response({'data':tempList})
        # if id:
        #     msg_obj = Sendmessage.objects.filter(id=id).values('id','def_message','def_message__default_message','driver')
        #     # print('dsahj',msg_obj)
        #     return Response({'data':msg_obj})
        # else:
        #     msg_obj = Sendmessage.objects.all().values('id','def_message','def_message__default_message','driver')
        #     return Response(msg_obj)
        return Response({'data':[[]]})
      
    def post(self,request):
        data=request.data
        def_message=data['def_message']
        # customise_msg=data['customise_msg']
        driver_id=data['driver_id']
        # print("driver_id=====>>>",driver_id)

        if Driver.objects.filter(user_id=data['driver_id']).exists():
            driver=Driver.objects.get(user_id=data['driver_id'])
            # print('=====<><>AAAAAAa',driver)
            remark_obj= Sendmessage.objects.create(def_message_id=def_message,driver_id=driver.id)
            return Response({'data':'Sendmessage Successfully Added!!'})
        return Response({'message':'Driver_id not found!!!'})

    def put(self,request,pk):
        data = request.data
        def_message=data['def_message']
        # customise_msg=data['customise_msg']
        driver_id=data['driver_id']
        # print("driver_id=====>>>",driver_id)

        if Driver.objects.filter(user_id=data['driver_id']).exists():
            driver=Driver.objects.get(user_id=data['driver_id'])
            Sendmessage.objects.filter(id=pk).update(def_message_id=def_message,driver_id=driver.id)
            return Response({'message': 'Sendmessage is updated'})
        else:
            return Response({'error':'Sendmessage id is not found'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        data = request.data
        if Sendmessage.objects.filter(id=pk).exists():
            Sendmessage.objects.filter(id=pk).delete()
            return Response({'message': 'Sendmessage is deleted'})
        else:
            return Response({'error':'Sendmessage id is not found'},status=status.HTTP_404_NOT_FOUND)

class getdrivermsgApi(APIView):
    def get(self,request):
        data = request.data
        id = request.query_params.get('id')
        driver_id=request.query_params.get('driver_id')
        default=request.query_params.get('default')
        # msg_obj = Defaultmessage.objects.all().values()
        if driver_id:
            msg_obj = Sendmessage.objects.filter(driver__user__id=driver_id).values('id','def_message','def_message__default_message','driver','customise_msg')
            # print('dsahj',driver_id)
            return Response({'data':msg_obj})
        return Response({'message':'driver_id not found!!'})

class MessageCustomised(APIView):
    def get(self,request):
        data = request.data
        id = request.query_params.get('id')
        driver_id=request.query_params.get('driver_id')
        default=request.query_params.get('default')
        # msg_obj = Defaultmessage.objects.all().values()
        if driver_id:
            tempList=[]
            msg_obj = Messagecustomised.objects.filter(driver__user__id=driver_id).values('id','customise_msg','driver')
            tempList.append(msg_obj)
            # print('dsahj',tempList)
            return Response({'data':tempList})
        if id:
            msg_obj = Messagecustomised.objects.filter(id=id).values('id','customise_msg','driver')
            # print('dsahj',msg_obj)
            return Response({'data':msg_obj})
        else:
            msg_obj = Messagecustomised.objects.all().values('id','customise_msg','driver')
            return Response(msg_obj)


    def post(self,request):
        data=request.data
        customise_msg=data['customise_msg']
        driver_id=data['driver_id']
        # print("driver_id=====>>>",driver_id)

        if Driver.objects.filter(user_id=data['driver_id']).exists():
            driver=Driver.objects.get(user_id=data['driver_id'])
            # print('=====<><>AAAAAAa',driver)
            remark_obj= Messagecustomised.objects.create(customise_msg=customise_msg,driver_id=driver.id)
            return Response({'data':'customise_msg Successfully Added!!'})
        return Response({'message':'Driver_id not found!!!'})
    
    def put(self,request,pk):
        data = request.data
        customise_msg=data['customise_msg']
        driver_id=data['driver_id']
        # print("driver_id=====>>>",driver_id)

        if Driver.objects.filter(user_id=data['driver_id']).exists():
            driver=Driver.objects.get(user_id=data['driver_id'])
            Messagecustomised.objects.filter(id=pk).update(customise_msg=customise_msg,driver_id=driver.id)
            return Response({'message': 'customise_msg is updated'})
        else:
            return Response({'error':'customise_msg id is not found'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        data = request.data
        if Messagecustomised.objects.filter(id=pk).exists():
            Messagecustomised.objects.filter(id=pk).delete()
            return Response({'message': 'customise_msg is deleted'})
        else:
            return Response({'error':'customise_msg id is not found'},status=status.HTTP_404_NOT_FOUND)

class DefaultmessageApi(APIView):
    def get(self,request):
        data = request.data
        default_message = request.query_params.get('default_message')
        id = request.query_params.get('id')
        if id:
            msg_obj = Defaultmessage.objects.filter(id = id).values()
            return Response({'data':msg_obj})
        else:
            msg_obj = Defaultmessage.objects.all().values()
            return Response({'data':msg_obj})

    def post(self,request):
        data = request.data
        default_message=data['default_message']
        msg_obj= Defaultmessage.objects.create(default_message=default_message)
        return Response({'data':'default_message Successfully Added!!'})

    def put(self,request,pk):
        data = request.data
        default_message=data['default_message']

        if Defaultmessage.objects.filter(id=pk).exists():
            Defaultmessage.objects.filter(id=pk).update(default_message=default_message)
            return Response({'message': 'default_message is updated'})
        else:
            return Response({'error':'default_message id is not found'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        data = request.data
        if Defaultmessage.objects.filter(id=pk).exists():
            Defaultmessage.objects.filter(id=pk).delete()
            return Response({'message': 'default_message is deleted'})
        else:
            return Response({'error':'default_message id is not found'},status=status.HTTP_404_NOT_FOUND)

class DriveryearApi(APIView):
    def get(self,request):
        year = request.query_params.get('year')
        # print("year", year, type(year))
        month = request.query_params.get('month')
        # print("month",month)
        week = request.query_params.get('week')
        # print("week",week)
        day=request.query_params.get('day')
        # print("day")
        driver_id=request.query_params.get('driver_id')
        month_wise_order_count=Driver.objects.filter(user__id=driver_id).values('create_timestamp')
        # print('ffffff',month_wise_order_count)
        tempList=[]
        for i in month_wise_order_count:
            tempList.append(i['create_timestamp'].year)
            # print('dddddd',tempList)
        return Response({'driver_year':tempList})





import datetime
# from .backgroundScheduler import *
import time
from datetime import datetime
from datetime import datetime, timedelta


# from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

# def stopScheduler():


class VehicleSubscriptionApi(APIView):
    def get(self, request):
        if request.query_params:
            datas = Vehicle_Subscription.objects.filter(vehicle_id_id=request.query_params['vehicle_id']).values().last()
            return Response({'data': datas})
        else:
            data = Vehicle_Subscription.objects.all().select_related('vehicle_id', 'vehicle_id__vehicletypes').values('id', 'vehicle_id__vehicle_name', 'time_period', 'date_subscribed', 'expiry_date', 'amount', 'status', 'is_amount_paid', 'paid_through', 'type_of_service', 'vehicle_id', 'validity_days', 'is_expired', 'vehicle_id__vehicle_number', 'vehicle_id__vehicletypes__vehicle_type_name')

            result = []
            for item in data:
                # Add driver information
                driver = Driver.objects.filter(vehicle=item['vehicle_id']).first()
                if driver:
                    item['driver_id'] = driver.id
                    item['driver_first_name'] = driver.user.first_name
                    item['driver_mobile_number'] = driver.user.mobile_number
                else:
                    item['driver_id'] = None
                    item['driver_first_name'] = None
                    item['driver_mobile_number'] = None

                result.append(item)

            return Response(result)

    def post(self,request):
        data=request.data
        time_period=data['time_period']
        date_subscribed=data.get('date_subscribed')
        # expiry_date=data['expiry_date']
        amount=data['amount']
        status=data.get('status')
        is_amount_paid=data.get('is_amount_paid')
        # paid_through=data.get('paid_through')
        type_of_service=data.get('type_of_service')
        vehicle_id=data.get('vehicle_id')
        validity_days=data.get('validity_days')
        # is_expired=data['is_expired']

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        payment = client.order.create({"amount": int(amount),"currency": "INR","payment_capture": "1"})

        # print("payment response from razor pay", payment)

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.order.create({"amount": int(amount), "currency": "INR", "payment_capture": "1"})

        if Vehicle.objects.filter(id=vehicle_id).exists():
            vehicle = Vehicle.objects.get(id=vehicle_id)

            if date_subscribed is not None:
                date_subscribed = date_subscribed.split('T')[0]  # Extract only the date part
                date_subscribed = datetime.strptime(date_subscribed, "%Y-%m-%d").date()

            validity_days = int(validity_days)  # Convert validity_days to an integer
            expiry_date = date_subscribed + timedelta(days=validity_days)

            now = datetime.now()
            expiry_date = datetime.combine(expiry_date, datetime.min.time())  # Convert expiry_date to a datetime object

            if now > expiry_date:
                status = 'Expired'
            else:
                status = 'Active'

            if data['vehicle_subscription_id'] is not None:
                obj = Vehicle_Subscription.objects.filter(id=data['vehicle_subscription_id']).update(
                    time_period=time_period,
                    date_subscribed=date_subscribed,
                    expiry_date=expiry_date,
                    amount=amount,
                    status=status,
                    is_amount_paid=is_amount_paid,
                    type_of_service=type_of_service,
                    validity_days=validity_days,
                    vehicle_id_id=vehicle_id
                )
                return Response({'order_id': payment['id']})
            else:
                obj = Vehicle_Subscription.objects.create(
                    time_period=time_period,
                    date_subscribed=date_subscribed,
                    expiry_date=expiry_date,
                    amount=amount,
                    status=status,
                    is_amount_paid=is_amount_paid,
                    type_of_service=type_of_service,
                    validity_days=validity_days,
                    vehicle_id_id=vehicle_id
                )
                return Response({'order_id': payment['id'], 'subscription_id': obj.id})

        return Response({'data': 'vehicle_id not found!!'})

    # def post(self,request):
    #     data=request.data
    #     time_period=data['time_period']
    #     date_subscribed=data.get('date_subscribed')
    #     # expiry_date=data['expiry_date']
    #     amount=data['amount']
    #     status=data.get('status')
    #     is_amount_paid=data.get('is_amount_paid')
    #     # paid_through=data.get('paid_through')
    #     type_of_service=data.get('type_of_service')
    #     vehicle_id=data.get('vehicle_id')
    #     validity_days=data.get('validity_days')
    #     # is_expired=data['is_expired']
    #
    #     client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    #
    #     payment = client.order.create({"amount": int(amount),"currency": "INR","payment_capture": "1"})
    #
    #     # print("payment response from razor pay", payment)
    #
    #     if Vehicle.objects.filter(id=vehicle_id).exists():
    #
    #         vehicle=Vehicle.objects.filter(id=vehicle_id)
    #         now = datetime.now()
    #         expirydate= now + datetime.timedelta(validity_days)
    #
    #         if data['vehicle_subscription_id'] is not None:
    #             if is_amount_paid:
    #                 obj=Vehicle_Subscription.objects.filter(id=data['vehicle_subscription_id']).update(
    #                     time_period=time_period,
    #                     date_subscribed=date_subscribed,
    #                     expiry_date=expirydate,
    #                     amount=amount,
    #                     status=status,
    #                     is_amount_paid=is_amount_paid,
    #                     type_of_service=type_of_service,
    #                     validity_days=validity_days,
    #                     vehicle_id_id=vehicle_id
    #                 )
    #             obj=Vehicle_Subscription.objects.filter(id=data['vehicle_subscription_id']).update(
    #                 time_period=time_period,
    #                 date_subscribed=date_subscribed,
    #                 expiry_date=expirydate,
    #                 amount=amount,
    #                 status=status,
    #                 type_of_service=type_of_service,
    #                 validity_days=validity_days,
    #                 vehicle_id_id=vehicle_id
    #             )
    #             return Response({'order_id':payment['id']})
    #         else:
    #             if is_amount_paid:
    #                 obj=Vehicle_Subscription.objects.create(
    #                     time_period=time_period,
    #                     date_subscribed=date_subscribed,
    #                     expiry_date=expirydate,
    #                     amount=amount,
    #                     status=status,
    #                     is_amount_paid=is_amount_paid,
    #                     type_of_service=type_of_service,
    #                     validity_days=validity_days,
    #                     vehicle_id_id=vehicle_id
    #                 )
    #             obj=Vehicle_Subscription.objects.create(
    #                 time_period=time_period,
    #                 date_subscribed=date_subscribed,
    #                 expiry_date=expirydate,
    #                 amount=amount,
    #                 status=status,
    #                 type_of_service=type_of_service,
    #                 validity_days=validity_days,
    #                 vehicle_id_id=vehicle_id
    #             )
    #             return Response({'order_id':payment['id'], 'subscription_id': obj.id})
    #     return Response({'data':'vehicle_id not found!!'})

    def put(self, request):
        ord_id=request.data['razorpay_order_id']
        raz_pay_id=request.data['razorpay_payment_id']
        raz_signature=request.data['razorpay_signature']
        is_amount_paid=request.data.get('is_amount_paid')
        driver_id = request.data['driver_id']
        subscription_id = request.data['subscription_id']

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        data = {
            'razorpay_order_id': ord_id,
            'razorpay_payment_id': raz_pay_id,
            'razorpay_signature': raz_signature
        }

        check = client.utility.verify_payment_signature(data)

        if check:
            PaymentDetails.objects.create(
                razorpay_order_id = ord_id,
                razorpay_payment_id = raz_pay_id,
                razorpay_signature = raz_signature,
                vehicle_subscription_id = subscription_id,
            )

            Vehicle_Subscription.objects.filter(id=subscription_id).update(
                is_amount_paid = is_amount_paid,
            )
        else:
            pass

        return Response("")

class SchedulehourApi(APIView):
    def get(self,request):
        data = request.data
        if request.query_params:
            query_obj = Schedulehour.objects.filter(id=request.query_params['id']).values('id','time')
            return Response({'data':query_obj})
        else:
            query_obj = Schedulehour.objects.all().values('id','time')
            return Response({'data':query_obj})

    def post(self,request):
        data = request.data
        time = data['time']

        if Schedulehour.objects.exists():
            return Response({'error':'Data already present in the DB!!'},status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            about = Schedulehour.objects.create(time=time)
            return Response({'message':'Successfully added Schedulehour'})

    def put(self,request,pk):
        data = request.data
        time=data.get('time')

        if Schedulehour.objects.filter(id=pk).exists():

            schedule_obj=Schedulehour.objects.filter(id=pk).update(time=time)
            return Response({'message':'Successfully update Schedulehour'})
        else:
            return Response({'error':'Schedulehour id not found'},status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk):
        data = request.data1
        if Schedulehour.objects.filter(id=pk).exists():
            Schedulehour.objects.filter(id=pk).delete()
            return Response({'message':'Successfully delete Schedulehour'})
        else:
            return Response({'error':'Schedulehour id not found!!'},status=status.HTTP_404_NOT_FOUND)


        

#======================================================================================================================================


from datetime import datetime

class History_of_SubscriptionplanApi(APIView):
    def get(self, request):
        driver_id = request.query_params.get('driver_id')
        try:
            driver = Driver.objects.get(user_id=driver_id)
            vehicle = driver.vehicle
            subscriptions = Vehicle_Subscription.objects.filter(vehicle_id=vehicle.id)
            print(subscriptions,"ssssssssssss")
            serialized_subscriptions = []
            for subscription in subscriptions:
                print(subscription.time_period,"subscription.time_periods==============")
                print(subscription.date_subscribed,"subscription.date_subscribed==========")
                print(subscription.expiry_date,"subscription.expiry_date")
                serialized_subscription = {
                    'time_period': subscription.time_period,
                    'date_subscribed': subscription.date_subscribed,
                    'expiry_date': subscription.expiry_date,
                    'amount': subscription.amount,
                    'status': subscription.status,
                    'is_amount_paid': subscription.is_amount_paid,
                    'paid_through': subscription.paid_through,
                    'type_of_service': subscription.type_of_service,
                    'validity_days': subscription.validity_days,
                    'is_expired': subscription.is_expired,
                    'driver_id': driver_id,  # add driver_id to the response
                    'driver_name': driver.user.first_name,
                    'vehicle_number': vehicle.vehicle_number,
                    'vehicle_name': vehicle.vehicle_name,
                    'mobile_number': driver.user.mobile_number,
                    'vehicle_type': vehicle.vehicletypes.vehicle_type_name,
                }
                serialized_subscriptions.append(serialized_subscription)
            response_data = {
                'subscriptions': serialized_subscriptions
            }
            return Response(response_data)
        except Driver.DoesNotExist:
            return Response(status=404, data={'message': 'Driver not found'})




# class History_of_SubscriptionplanApi(APIView):
#     def get(self, request):
#         driver_id = request.query_params.get('driver_id')
#         try:
#             driver = Driver.objects.get(user_id=driver_id)
#             vehicle = driver.vehicle
#             subscriptions = Vehicle_Subscription.objects.filter(vehicle_id=vehicle.id)
#             serialized_subscriptions = []
#             for subscription in subscriptions:
#                 current_date = datetime.now().date()
#                 expiry_date = subscription.expiry_date.date()  # Convert expiry_date to datetime.date object
#
#                 if current_date > expiry_date:
#                     status = 'Expired'
#                 else:
#                     status = 'Active'
#
#                 serialized_subscription = {
#                     'time_period': subscription.time_period,
#                     'date_subscribed': subscription.date_subscribed,
#                     'expiry_date': subscription.expiry_date,
#                     'amount': subscription.amount,
#                     'status': status,
#                     'is_amount_paid': subscription.is_amount_paid,
#                     'paid_through': subscription.paid_through,
#                     'type_of_service': subscription.type_of_service,
#                     'validity_days': subscription.validity_days,
#                     'is_expired': subscription.is_expired,
#                     'driver_id': driver_id,
#                     'driver_name': driver.user.first_name,
#                     'vehicle_number': vehicle.vehicle_number,
#                     'vehicle_name': vehicle.vehicle_name,
#                     'mobile_number': driver.user.mobile_number,
#                     'vehicle_type': vehicle.vehicletypes.vehicle_type_name,
#                 }
#                 serialized_subscriptions.append(serialized_subscription)
#
#             response_data = {
#                 'subscriptions': serialized_subscriptions
#             }
#             return Response(response_data)
#         except Driver.DoesNotExist:
#             return Response(status=404, data={'message': 'Driver not found'})

        # if year and status_id:
        #     status_id_list = re.findall(r'\d+', status_id)
        #     status_id_list = [int(num) for num in status_id_list]
        #     response_data = []
        #     for status_id in status_id_list:
        #         status_record = Status.objects.get(id=status_id)
        #         status_name = status_record.status_name
        #         color = color_dict.get(status_name)
        #         order_counts = {}
        #         for month in range(1, 13):
        #             days_in_month = calendar.monthrange(int(year), month)[1]
        #             for day in range(1, days_in_month + 1):
        #                 date = datetime.date(int(year), month, day)
        #                 orders = bookings.filter(
        #                     ordered_time__year=date.year,
        #                     ordered_time__month=date.month,
        #                     ordered_time__day=date.day,
        #                     status_id=status_id,
        #                 )
        #                 count = orders.count()
        #                 order_counts[date.strftime('%Y-%m-%d')] = count

        #         response_data.append({
        #             'status_name': status_name,
        #             'color': color,
        #             'order_counts': [{'date': date, 'count': order_counts.get(date, 0)} for date in order_counts.keys()]
        #         })
        #     return Response(response_data)
        # return Response([])  like ths i need to filter the dates             for booking in bookings:
        #         if booking['ordered_time'] and str(booking['ordered_time'].date()) == ordered_time: