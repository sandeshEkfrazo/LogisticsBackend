from django.contrib import admin
from .models import *


# Register your models here.

# @admin.register(UserRoleRef)
# class UserRoleRef(admin.ModelAdmin):
#     list_display = ['id','user_role_name','create_timestamp','last_update_timestamp']

# @admin.register(City)
# class City(admin.ModelAdmin):
#     list_display =['id','city_name']

# @admin.register(CustomUser)
# class CustomUser(admin.ModelAdmin):
#     list_display =['id','role','city','vehicle','first_name','last_name','mobile_number','company_name','email','alternate_number','zip_code','address','adhar_card','reset_otp','profile_image_path','base64','adhar_card_front_side_img','adhar_card_front_side_img_path','adhar_card_back_side_img','adhar_card_back_side_img_path','pan_card','pan_image_path','pan_card_base64','whatsup_number']

# @admin.register(Driver)
# class Driver(admin.ModelAdmin):
#     list_display =['id','user','account','vehicle','owner_id','subcription','account','notification_history','driver_driving_license','badge','driving_license_image_path','validity_start_date_time','validity_end_date_time','driver_status','license_expire_date','fitness_certificate_expire_date','insurance_expire_date','license_img_front','license_img_back','insurence_img','passbook_img','fitness_certificate_front_side_img_path','fitness_certificate_back_side_img_path','live_lattitude','live_longitude','date_online','date_offline','is_online','time','create_timestamp','last_update_timestamp']

# @admin.register(PaymentDetails)
# class PaymentDetails(admin.ModelAdmin):
#     list_dispaly = ['id','razorpay_order_id', 'razorpay_payment_id','razorpay_signature','vehicle_subscription' ]
