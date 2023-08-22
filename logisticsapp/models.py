import base64
from ctypes import addressof
from operator import mod
from turtle import up
from django.db import models
from django.contrib.auth.models import User
# from django.db.models.base import Model
from .models import *
from masters.models import *

#!------------------    MASTER TABLE    ------------------#!

class City(models.Model):
    city_name= models.CharField(max_length=250, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp")
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp")

class VehicleTypes(models.Model):
    vehicle_type_name= models.CharField(max_length=250, blank=True, null=True)
    capacity= models.CharField(max_length=250, blank=True, null=True)
    size = models.CharField(max_length=250, blank=True, null=True)
    details= models.CharField(max_length=250, blank=True, null=True)
    per_km_price= models.CharField(max_length=100, blank=True, null=True)
    per_min_price=models.CharField(max_length=100,blank=True,null=True)
    min_charge = models.CharField(max_length=100, blank=True, null=True)
    free_min=models.CharField(max_length=100, blank=True, null=True)
    max_time_min = models.CharField(max_length=100, blank=True, null=True)
    badge = models.CharField(max_length=100, blank=True, null=True) # (mandatory/not)
    vehicle_type_image=models.ImageField(blank=True, null=True)
    offer_price=models.CharField(max_length=100, blank=True, null=True)
    vehicle_type_sub_images=models.JSONField(null=True, blank=True)
    vehicle_description=models.JSONField(null=True,blank=True)
    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp")
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp")

    def __str__(self):
        return self.vehicle_type_name

#!------------------------------------------------------------------------#!
class Vehicle(models.Model):
    vehicletypes = models.ForeignKey(VehicleTypes, on_delete=models.CASCADE, blank=True, null=True, related_name='vehicletypes')
    vehicle_name = models.CharField(max_length=250, blank=True, null=True)
    vehicle_number = models.CharField(max_length=250, blank=True, null=True)
    vehicle_status = models.CharField(max_length=250, blank=True, null=True)
    # status = models.CharField(max_length=100, blank=True, null=True)

    # permit_front_side_img = models.TextField(blank=True, null=True)
    permit_front_side_img_path = models.FileField(blank=True, null=True)
    # permit_front_side_img_mandatory=models.BooleanField(default=True)
    permit_expire_date = models.DateField(null=True, blank=True)

    registration_certificate_front_side_img_path= models.FileField(blank=True, null=True)
    # registration_certificate_front_side_img_mandatory=models.BooleanField(default=True)
    registration_certificate_back_side_img_path= models.FileField(blank=True, null=True)
    # registration_certificate_back_side_img_mandatory=models.BooleanField(default=True)
    rc_expire_date = models.DateField(null=True, blank=True)

    pollution_certificate_front_side_img_path= models.FileField(blank=True, null=True)
    # pollution_certificate_front_side_img_mandatory=models.BooleanField(default=True)
    emission_test_expire_date = models.DateField(null=True, blank=True)

    # registration_certificate_back_side_img = models.TextField(blank=True, null=True)
    # registration_certificate_front_side_img = models.TextField(blank=True, null=True)
    # pollution_certificate_front_side_img = models.TextField(blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        if self.vehicle_name is not None:
            return self.vehicle_name
        else:
            return ""

class CustomUser(models.Model):
    # user  = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    role= models.ForeignKey(UserRoleRef, on_delete=models.CASCADE, blank=True, null=True, related_name="role")
    city= models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)

    # driver= models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True, related_name='vehicle')

    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    mobile_number=models.CharField(max_length=150, blank=True, null=True)
    company_name = models.CharField(max_length=250, blank=True, null=True)
    email= models.EmailField(max_length=250, blank=True, null=True)
    alternate_number= models.CharField(max_length=250, blank=True, null=True)
    zip_code= models.CharField(max_length=250, blank=True, null=True)
    address= models.CharField(max_length=250, blank=True, null=True)
    adhar_card= models.CharField(max_length=250, blank=True, null=True)
    reset_otp = models.CharField(max_length=100, null=True, blank=True)
    profile_image_path=models.TextField(blank=True, null=True)
    base64=  models.TextField(blank=True, null=True)

    profile_image = models.FileField(null=True, blank=True)

    adhar_card_front_side_img= models.TextField(blank=True, null=True)
    adhar_card_front_side_img_path= models.FileField(null=True, blank=True)
    # adhar_card_front_side_mandatory=models.BooleanField(default=True)
    
    adhar_card_back_side_img= models.TextField(blank=True, null=True)
    adhar_card_back_side_img_path= models.FileField(null=True, blank=True)
    # adhar_card_back_side_img_mandatory=models.BooleanField(default=True)

    pan_card= models.CharField(max_length=250, blank=True, null=True)
    pan_image_path=models.TextField(blank=True, null=True)
    pan_card_base64=  models.TextField(blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

    whatsup_number  = models.CharField(max_length=100, null=True, blank=True)

    user_status = models.CharField(max_length=100, null=True, blank=True)

    

  

class Driver(models.Model):

    user  = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True, related_name='types')
    owner_id= models.CharField(max_length=250, blank=True, null=True)
    subcription = models.ForeignKey(Subscriptionplan, on_delete=models.CASCADE, blank=True, null=True)
    notification_history  = models.CharField(max_length=3000, blank=True, null=True)

    driver_driving_license= models.CharField(max_length=250, blank=True, null=True)
    owner_driving_licence = models.CharField(max_length=100, null=True, blank=True)
    
    badge= models.CharField(max_length=250, blank=True, null=True)
    driving_license_image_path = models.CharField(max_length=250, blank=True, null=True)
    # base64=  models.TextField(max_length=50000, blank=True, null=True)

    # license_status= models.CharField(max_length=100, blank=True, null=True)

    validity_start_date_time= models.CharField(max_length=250, blank=True, null=True)
    validity_end_date_time = models.CharField(max_length=250, blank=True, null=True)
    driver_status = models.CharField(max_length=100, blank=True, null=True)
    date_online=models.DateTimeField(null=True, blank=True)
    date_offline=models.DateTimeField(null=True, blank=True)

    
    license_img_front = models.FileField(null=True, blank=True)
    # license_img_front_mandatory=models.BooleanField(default=False)
    license_img_back = models.FileField(null=True, blank=True)
    # license_img_back_license_mandatory=models.BooleanField(default=False)
    license_expire_date = models.DateField(null=True, blank=True)
    
    # emission_test_img = models.CharField(max_length=100, blank=True, null=True)
    insurence_img = models.FileField(blank=True, null=True)
    insurence_expire_date = models.DateField(null=True, blank=True)

    # rc_img = models.CharField(max_length=100, blank=True, null=True)

    passbook_img = models.FileField(blank=True, null=True)
    # passbook_img=models.BooleanField(default=True)

    # fitness_certificate_front_side_img = models.TextField(blank=True, null=True)
    fitness_certificate_front_side_img_path = models.FileField(blank=True, null=True)
    # fitness_certificate_front_side_img_mandatory=models.BooleanField(default=True)
    fitness_certificate_back_side_img_path = models.FileField(blank=True, null=True)
    # fitness_certificate_back_side_img_mandatory=models.BooleanField(default=True)
    fitness_certificate_expire_date = models.DateField(null=True, blank=True)
    

    live_lattitude = models.CharField(max_length=100, blank=True, null=True)
    live_longitude = models.CharField(max_length=100, blank=True, null=True)

    is_online = models.BooleanField(default=False)
    time=models.IntegerField(blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

    is_active = models.BooleanField(default=True)

class Customised_message(models.Model):
    driver=models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True,null=True)
    # name = models.CharField(max_length=100, blank=True, null=True)
    message_type=models.CharField(max_length=100, blank=True, null=True)

class DriverDocumentStatus(models.Model):
    status_name = models.CharField(max_length=100, blank=True, null=True)
    # due_date = models.CharField(max_length=100,blank=True,null=True)
    # label = models.CharField(max_length=100,blank=True,null=True)
    # description = models.CharField(max_length=100,blank=True,null=True)
    # descriptions = models.CharField(max_length=100, blank=True, null=True)   

class Remarks(models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True,null=True)
    document_status=models.ForeignKey(DriverDocumentStatus, on_delete=models.CASCADE, blank=True,null=True)
    text=models.CharField(max_length=100, blank=True, null=True) 

class DriverDocumentExpiryvalidity(models.Model):
    due_date = models.CharField(max_length=100,blank=True,null=True)
    label = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=100,blank=True,null=True)
    # number_of_days=models.CharField(max_length=100,blank=True,null=True)

class Vehicle_Subscription(models.Model):
    time_period=models.CharField(max_length=100,blank=True,null=True)
    date_subscribed=models.DateTimeField(max_length=100,blank=True,null=True)
    expiry_date=models.DateTimeField(max_length=100,blank=True,null=True)
    amount=models.CharField(max_length=100,blank=True,null=True)
    status=models.CharField(max_length=100,blank=True,null=True)
    is_amount_paid=models.BooleanField(default=False)
    paid_through=models.CharField(max_length=100,blank=True,null=True)
    type_of_service=models.CharField(max_length=100,blank=True,null=True)
    vehicle_id=models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True,null=True)
    validity_days=models.IntegerField(blank=True,null=True)
    is_expired=models.BooleanField(default=False)

class PaymentDetails(models.Model):
    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=200, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=200, null=True, blank=True)
    vehicle_subscription = models.ForeignKey(Vehicle_Subscription, on_delete=models.CASCADE, blank=True, null=True)

class Schedulehour(models.Model):
    time=models.TimeField(blank=True, null=True)