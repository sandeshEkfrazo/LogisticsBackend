import base64
from ctypes import addressof
from operator import mod
from turtle import up
from django.db import models
from django.contrib.auth.models import User
# from django.db.models.base import Model
from .models import *

#!------------------    MASTER TABLE    ------------------#!


class UserRoleRef(models.Model):
    user_role_name = models.CharField(max_length=250, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp")
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp")

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

class Coupons(models.Model):

    coupon_name= models.CharField(max_length=250, blank=True, null=True)
    coupon_discount= models.CharField(max_length=250, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp")
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp")

class Status(models.Model):

    status_name= models.CharField(max_length=250, blank=True, null=True)
    colour = models.CharField(max_length=250, blank=True, null=True)
    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)


class Subscription(models.Model):

    sub_plan_name= models.CharField(max_length=250, blank=True, null=True)
    price= models.CharField(max_length=250, blank=True, null=True)
    validity_period= models.CharField(max_length=250, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

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

class Account(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='User')
    acc_holder_name = models.CharField(max_length=100, blank=True, null=True)
    bank = models.CharField(max_length=100, blank=True, null=True)
    branch = models.CharField(max_length=100, blank=True, null=True)
    account_no = models.CharField(max_length=100, blank=True, null=True)
    ifsc_code = models.CharField(max_length=100, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)


class CustomUser(models.Model):
    # user  = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    role= models.ForeignKey(UserRoleRef, on_delete=models.CASCADE, blank=True, null=True)
    city= models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)

    # driver= models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True)

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

class Driver(models.Model):

    user  = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    account  = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True, related_name='types')
    owner_id= models.CharField(max_length=250, blank=True, null=True)
    subcription = models.ForeignKey(Subscription, on_delete=models.CASCADE, blank=True, null=True)
    account  = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    notification_history  = models.CharField(max_length=3000, blank=True, null=True)

    driver_driving_license= models.CharField(max_length=250, blank=True, null=True)
    
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


class OrderDeatil(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True)
    vehicle_number = models.CharField(max_length=200, null=True, blank=True)
    location_details = models.JSONField(null=True, blank=True)
    # date=models.DateField(null=True, blank=True)
    notification_history  = models.CharField(max_length=3000, blank=True, null=True)

class Notification(models.Model):
    order_detail = models.ForeignKey(OrderDeatil, on_delete=models.CASCADE, blank=True, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    order_status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True)

    driver_list = models.CharField(max_length=300, null=True, blank=True)
    user_list = models.CharField(max_length=300, null=True, blank=True)
    notification_message = models.CharField(max_length=300, null=True, blank=True)
    send_to = models.CharField(max_length=100, null=True, blank=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

class Review(models.Model):

    review_stars = models.CharField(max_length=250, blank=True, null=True)
    comment = models.CharField(max_length=250, blank=True, null=True)
    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp")
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp")
    review_type = models.CharField(max_length=250, blank=True, null=True)
    linked_id = models.CharField(max_length=250, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

class CustomerAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    label= models.CharField(max_length=250, blank=True, null=True)
    house_number= models.CharField(max_length=250, blank=True, null=True)
    address= models.CharField(max_length=250, blank=True, null=True)
    area= models.CharField(max_length=250, blank=True, null=True)
    landmark= models.CharField(max_length=250, blank=True, null=True)

    zipcode= models.CharField(max_length=250, blank=True, null=True)
    latitude= models.CharField(max_length=250, blank=True, null=True)
    longitude= models.CharField(max_length=250, blank=True, null=True)
    contact_number= models.CharField(max_length=250, blank=True, null=True)
    contact_name= models.CharField(max_length=250, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)


class PickupDetails(models.Model):
    customer_address  = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE, blank=True, null=True)

    pickup_date = models.CharField(max_length=250, blank=True, null=True)
    pickup_time = models.CharField(max_length=250, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

class DropDetails(models.Model):

    customer_address  = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE, blank=True, null=True)
    drop_date = models.CharField(max_length=250, blank=True, null=True)
    drop_time = models.CharField(max_length=250, blank=True, null=True)
    priority = models.CharField(max_length=250, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

class PlacedOrder(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    pickup = models.ForeignKey(PickupDetails, on_delete=models.CASCADE, blank=True, null=True)
    vehicle_type = models.ForeignKey(VehicleTypes, on_delete=models.CASCADE, blank=True, null=True)
    drop= models.CharField(max_length=250, blank=True, null=True)

    estimated_kms = models.CharField(max_length=250, blank=True, null=True)
    estimated_amount = models.CharField(max_length=250, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

class InOrder(models.Model):

    placed_order= models.ForeignKey(PlacedOrder, on_delete=models.CASCADE, blank=True, null=True)
    coupon= models.ForeignKey(Coupons, on_delete=models.CASCADE, blank=True, null=True)
    driver= models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    status_details= models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True)

    final_amount= models.CharField(max_length=250, blank=True, null=True)
    comment= models.CharField(max_length=250, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

class PaymentDetails(models.Model):

    in_order  = models.ForeignKey(InOrder, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.CharField(max_length=250, blank=True, null=True)
    provider = models.CharField(max_length=250, blank=True, null=True)
    payment_status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True, null=True)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)

# class OrderDetail(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True)
#     vehicle_number = models.CharField(max_length=200, null=True, blank=True)
#     location_details = models.JSONField(null=True, blank=True)

# class PickupTable(models.Model):
#     p_one = models.CharField(max_length=100, blank=True, null=True)
#     p_two = models.CharField(max_length=100, blank=True, null=True)

# class DroupTable(models.Model):
#     d_one = models.CharField(max_length=100, blank=True, null=True)
#     d_two = models.CharField(max_length=100, blank=True, null=True)

class Queries(models.Model):
    questions = models.CharField(max_length=100, blank=True, null=True)
    answer = models.TextField(blank=True, null=True) 
    isfor = models.ForeignKey(UserRoleRef, on_delete=models.CASCADE, blank=True, null=True)
    status= models.CharField(max_length=100, blank=True, null=True)
    # user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True)

class Aboutus(models.Model):
    logo = models.ImageField(blank=True, null=True)
    heading = models.CharField(max_length=300, blank=True, null=True)
    paragraph = models.TextField(blank=True, null=True)
    phone_number=models.CharField(max_length=10, blank=True, null=True)
    alternate_phone_number=models.CharField(max_length=10, blank=True, null=True)
    text=models.TextField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

class Customised_message(models.Model):
    driver=models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True,null=True)
    # name = models.CharField(max_length=100, blank=True, null=True)
    message_type=models.CharField(max_length=100, blank=True, null=True)

# class accept_or_decline(models.Model):
#     vehicle_status = models.CharField(max_length=100, blank=True, null=True)
#     status = models.CharField(max_length=100, blank=True, null=True)
# class DriverQuries(models.Model):
#     questions = models.CharField(max_length=100, blank=True, null=True)
#     answer = models.TextField(blank=True, null=True) 
#     driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True,null=True)

class DriverDocumentStatus(models.Model):
    status_name = models.CharField(max_length=100, blank=True, null=True)
    # due_date = models.CharField(max_length=100,blank=True,null=True)
    # label = models.CharField(max_length=100,blank=True,null=True)
    # description = models.CharField(max_length=100,blank=True,null=True)
    # descriptions = models.CharField(max_length=100, blank=True, null=True)   

class Filesize(models.Model):
    file_type = models.CharField(max_length=100, blank=True, null=True) 
    size = models.CharField(max_length=100, blank=True, null=True) 

class Remarks(models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True,null=True)
    document_status=models.ForeignKey(DriverDocumentStatus, on_delete=models.CASCADE, blank=True,null=True)
    text=models.CharField(max_length=100, blank=True, null=True) 

class DriverDocumentExpiryvalidity(models.Model):
    due_date = models.CharField(max_length=100,blank=True,null=True)
    label = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=100,blank=True,null=True)
    # number_of_days=models.CharField(max_length=100,blank=True,null=True)

class Defaultmessage(models.Model):
    default_message=models.CharField(max_length=100,blank=True,null=True)

class Sendmessage(models.Model): 
    def_message=models.ForeignKey(Defaultmessage, on_delete=models.CASCADE, blank=True,null=True)
    driver=models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True,null=True)
    
class Messagecustomised(models.Model):
    customise_msg=models.CharField(max_length=100,blank=True,null=True)
    driver=models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True,null=True)

class Master(models.Model):
    language_name=models.CharField(max_length=100,blank=True,null=True)

class Subscriptionplan(models.Model):
    time_period=models.CharField(max_length=100,blank=True,null=True)
    validity_days=models.IntegerField(blank=True, null=True)
    amount=models.CharField(max_length=100,blank=True,null=True)
    type_of_service= models.CharField(max_length=100,blank=True,null=True)
    status=models.CharField(max_length=100,blank=True,null=True)

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

class Language(models.Model):
    name=models.CharField(max_length=200, null=True, blank=True)






# class VehicleTypes(models.Model):
#     vehicle_type_name= models.CharField(max_length=250, blank=True, null=True)
#     capacity= models.CharField(max_length=250, blank=True, null=True)
#     size = models.CharField(max_length=250, blank=True, null=True)
#     details= models.CharField(max_length=250, blank=True, null=True)

# class CustomUser(models.Model):
#     # user  = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     role= models.ForeignKey(UserRoleRef, on_delete=models.CASCADE, blank=True, null=True)
#     city= models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)

#     # driver= models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True)

#     first_name = models.CharField(max_length=250, blank=True, null=True)
#     last_name = models.CharField(max_length=250, blank=True, null=True)
#     mobile_number=models.CharField(max_length=150, blank=True, null=True)
# class Vehicle_Subscription(models.Model):
#     time_period=models.CharField(max_length=100,blank=True,null=True)
#     date_subscribed=models.DateTimeField(max_length=100,blank=True,null=True)
#     expiry_date=models.DateTimeField(max_length=100,blank=True,null=True)
#     amount=models.CharField(max_length=100,blank=True,null=True)
#     status=models.CharField(max_length=100,blank=True,null=True)
#     is_amount_paid=models.BooleanField(default=False)
#     paid_through=models.CharField(max_length=100,blank=True,null=True)
#     type_of_service=models.CharField(max_length=100,blank=True,null=True)
#     vehicle_id=models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True,null=True)
#     validity_days=models.IntegerField(blank=True,null=True)
#     is_expired=models.BooleanField(default=False)
#     class Driver(models.Model):

# user  = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
#     account  = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True, null=True, related_name='types')
#     owner_id= models.CharField(max_length=250, blank=True, null=True)
#     subcription = models.ForeignKey(Subscription, on_delete=models.CASCADE, blank=True, null=True)
# class Vehicle(models.Model):
#     vehicletypes = models.ForeignKey(VehicleTypes, on_delete=models.CASCADE, blank=True, null=True, related_name='vehicletypes')
#     vehicle_name = models.CharField(max_length=250, blank=True, null=True)
#     vehicle_number = models.CharField(max_length=250, blank=True, null=True)
#     vehicle_status = models.CharField(max_length=250, blank=True, null=True)
# class History_of_SubscriptionplanApi(APIView):
#     def get(self, request):
#         driver_id = request.query_params.get('driver_id')
#         try:
#             driver = Driver.objects.get(user_id=driver_id)
#             vehicle = driver.vehicle
#             subscriptions = Vehicle_Subscription.objects.filter(vehicle_id=vehicle.id)
#             serialized_subscriptions = []
#             for subscription in subscriptions:
#                 serialized_subscription = {
#                     'time_period': subscription.time_period,
#                     'date_subscribed': subscription.date_subscribed,
#                     'expiry_date': subscription.expiry_date,
#                     'amount': subscription.amount,
#                     'status': subscription.status,
#                     'is_amount_paid': subscription.is_amount_paid,
#                     'paid_through': subscription.paid_through,
#                     'type_of_service': subscription.type_of_service,
#                     'validity_days': subscription.validity_days,
#                     'is_expired': subscription.is_expired,
#                     'driver_id': driver_id,  # add driver_id to the response
#                     'driver_name': driver.user.first_name,
#                     'vehicle_number': vehicle.vehicle_number,
#                     'vehicle_name': vehicle.vehicle_name,
#                     'mobile_number': driver.user.mobile_number
#                 }
#                 serialized_subscriptions.append(serialized_subscription)
#             response_data = {
#                 'subscriptions': serialized_subscriptions
#             }
#             return Response(response_data)
#         except Driver.DoesNotExist:
#             return Response(status=404, data={'message': 'Driver not found'})
