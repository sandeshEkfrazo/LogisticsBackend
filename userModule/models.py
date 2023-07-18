from django.db import models
from logisticsapp.models import *
from django_celery_beat.models import ClockedSchedule, CrontabSchedule, PeriodicTask

# Create your models here.
class OrderDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True)
    vehicle_number = models.CharField(max_length=200, null=True, blank=True)
    location_detail = models.JSONField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    total_estimated_cost = models.FloatField(null=True, blank=True)

class BookingDetail(models.Model):
    order = models.ForeignKey(OrderDetails,on_delete=models.CASCADE, blank=True,null=True )
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True)
    status = models.ForeignKey(Status,on_delete=models.CASCADE,blank=True,null=True)
    total_amount = models.CharField(max_length=250, blank=True, null=True)
    travel_details = models.CharField(max_length=200, null=True, blank=True)

    is_bill_required = models.BooleanField(default=False)
    is_bill_recived = models.BooleanField(default=False)

    create_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="create_timestamp",blank=True, null=True)
    last_update_timestamp= models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)
    request_cancel = models.CharField(max_length=100,blank=True,null=True,)

    ordered_time = models.DateTimeField(blank=True, null=True)
    pickedup_time = models.DateTimeField(blank=True, null=True)
    order_accepted_time = models.DateTimeField(blank=True, null=True)
    canceled_time = models.DateTimeField(blank=True, null=True)
    order_droped_time = models.DateTimeField(blank=True, null=True)
    # inprogress_time = models.DateTimeField(blank=True, null=True)
    declined_time = models.DateTimeField(blank=True, null=True)
    trip_ended_time = models.DateTimeField(blank=True, null=True)
    request_canceled_ride_time = models.DateTimeField(blank=True, null=True)
    accept_canceled_ride_time = models.DateTimeField(blank=True, null=True)
    decline_canceled_ride_time = models.DateTimeField(blank=True, null=True)

    sub_user_phone_numbers = models.JSONField(null=True, blank=True)
    actual_time_taken_to_complete = models.CharField(max_length=200, null=True, blank=True)

    actual_time_taken_to_complete = models.CharField(max_length=200, null=True, blank=True)
    total_amount_without_actual_time_taken = models.FloatField(null=True, blank=True)

    is_scheduled = models.BooleanField(default=False)

class ScheduledOrder(models.Model):
    booking = models.ForeignKey(BookingDetail, on_delete=models.CASCADE, blank=True, null=True)
    scheduled_date_and_time = models.DateTimeField(blank=True, null=True)
    periodic_task = models.ForeignKey(PeriodicTask, on_delete=models.CASCADE, blank=True, null=True)


class UserFeedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True, related_name='user_id')
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True, related_name='driver_id')
    rating = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    review = models.CharField(max_length=200, null=True, blank=True)
    order = models.ForeignKey(OrderDetails, on_delete=models.CASCADE, null=True, blank=True)
    rating_given_by = models.TextField(null=True, blank=True)

class statusRecord(models.Model):
    order = models.ForeignKey(OrderDetails,on_delete=models.CASCADE, blank=True,null=True )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True, related_name='users' )
    status = models.ForeignKey(Status,on_delete=models.CASCADE,blank=True,null=True)
    is_accepted = models.BooleanField(default=False)
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True, related_name='drivers')
    
class VehicleAssingedToDriver(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE, blank=True,null=True)
    old_driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True, related_name='old_driver')
    new_driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True,null=True, related_name='new_driver')

    assigned_date_and_time = models.DateTimeField(auto_now_add=True,verbose_name="last_update_timestamp",blank=True, null=True)
