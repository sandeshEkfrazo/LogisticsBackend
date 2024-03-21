from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(BookingDetail)
class BookingDetail(ImportExportModelAdmin):
    list_display = ['id','order','driver', 'status', 'total_amount', 'create_timestamp', 'last_update_timestamp', 'travel_details', 'is_bill_required', 'is_bill_recived', 'request_cancel', 'ordered_time','pickedup_time','order_accepted_time','canceled_time','declined_time','trip_ended_time','request_canceled_ride_time','accept_canceled_ride_time','decline_canceled_ride_time','order_droped_time', 'sub_user_phone_numbers', 'actual_time_taken_to_complete', 'total_amount_without_actual_time_taken', 'is_scheduled', 'vehicle_type', 'is_all_mobile_number_verified']
    


@admin.register(OrderDetails)
class OrderDeatils(ImportExportModelAdmin):
    list_display = ['id','user','vehicle_number','location_detail', 'otp', 'total_estimated_cost']

@admin.register(UserFeedback)
class UserFeedback(ImportExportModelAdmin):
    list_display = ('id','user_id', 'driver','rating','review' ,'order', 'rating_given_by')

@admin.register(CheckOrderOTP)
class CheckOrderOTP(ImportExportModelAdmin):
    list_display = ('id','order', 'otp_json')

@admin.register(ScheduledOrder)
class ScheduledOrder(ImportExportModelAdmin):
    list_display = ['id','booking','scheduled_date_and_time', 'periodic_task']

@admin.register(statusRecord)
class statusRecord(ImportExportModelAdmin):
    list_display = ['id','order','user','status', 'is_accepted', 'driver']

@admin.register(VehicleAssingedToDriver)
class VehicleAssingedToDriver(ImportExportModelAdmin):
    list_display = ['id','vehicle_id', 'vehicle_id_id','old_driver','new_driver', 'assigned_date_and_time']
