from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
from import_export.admin import ImportExportModelAdmin
from masters.models import *

@admin.register(City)
class City(admin.ModelAdmin):
    list_display =['id','city_name']

@admin.register(CustomUser)
class CustomUser(admin.ModelAdmin):
    def user_role_name(self, obj):
        return obj.role.user_role_name

    # def vehicle_name(self, obj):
    #     return obj.vehicle.vehicle_name

    list_display =['id','user_role_name','city','vehicle','first_name','last_name','mobile_number','company_name','email','alternate_number','zip_code','address','adhar_card','reset_otp','profile_image_path','base64','adhar_card_front_side_img','adhar_card_front_side_img_path','adhar_card_back_side_img','adhar_card_back_side_img_path','pan_card','pan_image_path','pan_card_base64','whatsup_number', 'user_status', 'user_active_status']

@admin.register(VehicleTypes)
class VehicleTypes(ImportExportModelAdmin):
    list_display =['id','vehicle_type_name','capacity','size','details','per_km_price','per_min_price','min_charge','free_min','max_time_min','badge','vehicle_type_image','offer_price',]

@admin.register(Vehicle)
class Vehicle(admin.ModelAdmin):
    list_display =['id','vehicletypes','vehicle_name','vehicle_number','permit_front_side_img_path','vehicle_status','permit_expire_date','registration_certificate_front_side_img_path','registration_certificate_back_side_img_path','rc_expire_date','pollution_certificate_front_side_img_path', 'emission_certificate_expire_date']

@admin.register(Driver)
class Driver(admin.ModelAdmin):
    list_display =['id','user','vehicle','owner_id','subcription','notification_history','driver_driving_license', 'owner_driving_licence','badge','driving_license_image_path','validity_start_date_time','validity_end_date_time','driver_status','license_expire_date','fitness_certificate_expire_date','insurance_expire_date','license_img_front','license_img_back','insurence_img','passbook_img','fitness_certificate_front_side_img_path','fitness_certificate_back_side_img_path','live_lattitude','live_longitude','date_online','date_offline','is_online','time','create_timestamp','last_update_timestamp']

    def passbook_img(self, obj):
        print("====>>", obj)
        if obj.image:  # Assuming the name of your FileField is 'image'
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" />')
        else:
            return "No Image"

    passbook_img.short_description = 'Image'

@admin.register(Customised_message)
class Customised_message(admin.ModelAdmin):
    list_display = ['id','driver_id','message_type']


@admin.register(DriverDocumentStatus)
class DriverDocumentStatus(admin.ModelAdmin):
    list_display =['id','status_name']


@admin.register(Remarks)
class Remarks(admin.ModelAdmin):
    list_display =['id','driver_id','document_status','text']

@admin.register(DriverDocumentExpiryvalidity)
class DriverDocumentExpiryvalidity(admin.ModelAdmin):
    list_dispaly=['id','due_date','label','description']


@admin.register(Vehicle_Subscription)
class Vehicle_Subscription(ImportExportModelAdmin):
    list_dispaly = ['time_period','date_subscribed','expiry_date','amount','status','is_amount_paid','paid_through','type_of_service','vehicle_id','validity_days','is_expired']

@admin.register(Schedulehour)
class Schedulehour(admin.ModelAdmin):
    list_dispaly = ['id','time']

