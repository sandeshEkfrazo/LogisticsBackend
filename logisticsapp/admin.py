from django.contrib import admin
from django.contrib.auth.models import User


from .models import *






@admin.register(UserRoleRef)
class UserRoleRef(admin.ModelAdmin):
    list_display = ['id','user_role_name','create_timestamp','last_update_timestamp']



@admin.register(City)
class City(admin.ModelAdmin):
    list_display =['id','city_name']

@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    list_display =['id','role','city','vehicle','first_name','last_name','mobile_number','company_name','email','alternate_number','zip_code','address','adhar_card','reset_otp','profile_image_path','base64','adhar_card_front_side_img','adhar_card_front_side_img_path','adhar_card_back_side_img','adhar_card_back_side_img_path','pan_card','pan_image_path','pan_card_base64','whatsup_number']

@admin.register(VehicleTypes)
class VehicleTypes(admin.ModelAdmin):
    list_display =['id','vehicle_type_name','capacity','size','details','per_km_price','per_min_price','min_charge','free_min','max_time_min','badge','vehicle_type_image','offer_price',]

@admin.register(Vehicle)
class Vehicle(admin.ModelAdmin):
    list_display =['id','vehicletypes','vehicle_name','vehicle_number','permit_front_side_img_path','vehicle_status','permit_expire_date','registration_certificate_front_side_img_path','registration_certificate_back_side_img_path','rc_expire_date','pollution_certificate_front_side_img_path', 'emission_test_expire_date']

@admin.register(Review)
class Review(admin.ModelAdmin):
    list_display =['id','review_stars','comment','review_type','linked_id']

@admin.register(Driver)
class Driver(admin.ModelAdmin):
    list_display =['id','user','account','vehicle','owner_id','subcription','account','notification_history','driver_driving_license','badge','driving_license_image_path','validity_start_date_time','validity_end_date_time','driver_status','license_expire_date','fitness_certificate_expire_date','insurence_expire_date','license_img_front','license_img_back','insurence_img','passbook_img','fitness_certificate_front_side_img_path','fitness_certificate_back_side_img_path','live_lattitude','live_longitude','date_online','date_offline','is_online','time','create_timestamp','last_update_timestamp']

@admin.register(CustomerAddress)
class CustomerAddress(admin.ModelAdmin):
    list_display =['id','user','city','label','house_number','address','area','landmark','zipcode','latitude','longitude','contact_number','contact_name']

@admin.register(PickupDetails)
class PickupDetails(admin.ModelAdmin):
    list_display =['id','customer_address','pickup_date','pickup_time']
    
@admin.register(DropDetails)
class DropDetails(admin.ModelAdmin):
    list_display =['id','customer_address','drop_date','drop_time','priority']

@admin.register(PlacedOrder)
class PlacedOrder(admin.ModelAdmin):
    list_display =['id','user','pickup','vehicle_type','drop','estimated_kms','estimated_amount']   

@admin.register(Coupons)
class Coupons(admin.ModelAdmin):
    list_display =['id','coupon_name','coupon_discount']

@admin.register(Status)
class Status(admin.ModelAdmin):
    list_display =['id','status_name']

# @admin.register(Subscription)
# class Subscription(admin.ModelAdmin):
#     list_display =['id','sub_plan_name','price','validity_period']

@admin.register(InOrder)
class InOrder(admin.ModelAdmin):
    list_display =['id','placed_order','coupon','driver','status_details','final_amount','comment']

@admin.register(Queries)
class Queries(admin.ModelAdmin):
    list_display =['id','questions','answer','isfor','status']

@admin.register(Aboutus)
class Aboutus(admin.ModelAdmin):
    list_display = ['id','logo','heading','paragraph','phone_number','email','alternate_phone_number','text']

@admin.register(Customised_message)
class Customised_message(admin.ModelAdmin):
    list_display = ['id','driver_id','message_type']

# @admin.register(accept_or_decline)
# class accept_or_decline(admin.ModelAdmin):
#     list_display = ['id','vehicle_status','status']

# @admin.register(DriverQuries)
# class DriverQuries(admin.ModelAdmin):
#     list_display =['id','questions','answer','driver_id']

@admin.register(DriverDocumentStatus)
class DriverDocumentStatus(admin.ModelAdmin):
    list_display =['id','status_name']

@admin.register(Filesize)
class Filesize(admin.ModelAdmin):
    list_display =['id','file_type','size']

@admin.register(Remarks)
class Remarks(admin.ModelAdmin):
    list_display =['id','driver_id','document_status','text']

@admin.register(DriverDocumentExpiryvalidity)
class DriverDocumentExpiryvalidity(admin.ModelAdmin):
    list_dispaly=['id','due_date','label','description']

@admin.register(Defaultmessage)
class Defaultmessage(admin.ModelAdmin):
    list_dispaly=['id','default_message']

@admin.register(Sendmessage)
class Sendmessage(admin.ModelAdmin):
    list_dispaly=['id','def_message','driver']

@admin.register(Messagecustomised)
class MessageCustomised(admin.ModelAdmin):
    list_dispaly=['id','customise_msg','driver']

@admin.register(Master)
class Master(admin.ModelAdmin):
    list_dispaly=['id','language_name']

@admin.register(Subscriptionplan)
class Subscriptionplan(admin.ModelAdmin):
    list_dispaly=['id','time_period','validity_days','amount','type_of_service','status']

@admin.register(Vehicle_Subscription)
class Vehicle_Subscription(admin.ModelAdmin):
    list_dispaly=['time_period','date_subscribed','expiry_date','amount','status','is_amount_paid','paid_through','type_of_service','vehicle_id','validity_days','is_expired']

@admin.register(PaymentDetails)
class PaymentDetails(admin.ModelAdmin):
    list_dispaly = ['id','razorpay_order_id', 'razorpay_payment_id','razorpay_signature','vehicle_subscription' ]

@admin.register(Schedulehour)
class Schedulehour(admin.ModelAdmin):
    list_dispaly = ['id','time']

@admin.register(Language)
class Language(admin.ModelAdmin):
    list_dispaly = ['id','name']