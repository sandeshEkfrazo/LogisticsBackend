from django.db.models import fields
# from fitbit.views import getactivitylog
from .models import *
from  rest_framework import serializers
from userModule.serializers import *

class DriverSerializer(serializers.ModelSerializer):
    requirement_form = ScheduledOrderSerializer(read_only=True, many=True)
    class Meta:
        model = Driver
        fields = '__all__'




class DriversSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.IntegerField(source='vehicle.id', read_only=True)
    vehicle__vehicle_status = serializers.StringRelatedField(source='vehicle.vehicle_status', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user__role__id = serializers.IntegerField(source='user.role.id', read_only=True)
    user__first_name = serializers.StringRelatedField(source='user.first_name', read_only=True)
    user__mobile_number = serializers.StringRelatedField(source='user.mobile_number', read_only=True)
    vehicle__vehicle_name = serializers.StringRelatedField(source='vehicle.vehicle_name', read_only=True)

    vehicle__vehicle_number = serializers.StringRelatedField(source='vehicle.vehicle_number', read_only=True)
    vehicle__permit_front_side_img_path = serializers.StringRelatedField(source='vehicle.permit_front_side_img_path', read_only=True)
    vehicle__pollution_certificate_front_side_img_path = serializers.StringRelatedField(source='vehicle.pollution_certificate_front_side_img_path', read_only=True)
    vehicle__registration_certificate_back_side_img_path = serializers.StringRelatedField(source='vehicle.registration_certificate_back_side_img_path', read_only=True)
    vehicle__registration_certificate_front_side_img_path = serializers.StringRelatedField(source='vehicle.registration_certificate_front_side_img_path', read_only=True)
    vehicle__vehicletypes__vehicle_type_name = serializers.StringRelatedField(source='vehicle.vehicletypes.vehicle_type_name', read_only=True)
    vehicle__permit_expire_date = serializers.StringRelatedField(source='vehicle.permit_expire_date', read_only=True)
    vehicle__rc_expire_date = serializers.StringRelatedField(source='vehicle.rc_expire_date', read_only=True)
    vehicle__emission_certificate_expire_date = serializers.StringRelatedField(source='vehicle.emission_certificate_expire_date', read_only=True)
    class Meta:
        model = Driver
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleTypes
        fields = '__all__'

class VehicleSubscriptionSerializer(serializers.ModelSerializer):
    vehicle_id__vehicle_name = serializers.StringRelatedField(source='vehicle_id.vehicle_name', read_only=True)
    vehicle_id__vehicle_number = serializers.StringRelatedField(source='vehicle_id.vehicle_number', read_only=True)
    vehicle_id__vehicletypes__vehicle_type_name = serializers.StringRelatedField(source='vehicle_id.vehicletypes.vehicle_type_name', read_only=True)
    class Meta:
        model = Vehicle_Subscription
        fields = '__all__'

class VehicleSubscriptionHistorySerializer(serializers.ModelSerializer):
    vehicle_number = serializers.StringRelatedField(source='vehicle_id.vehicle_number', read_only=True)
    vehicle_name =  serializers.StringRelatedField(source='vehicle_id.vehicle_name', read_only=True)
    vehicle_type = serializers.StringRelatedField(source='vehicle_id.vehicletypes.vehicle_type_name', read_only=True)
    class Meta:
        model = Vehicle_Subscription
        fields = '__all__'

class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class BookingDetailSerializer(serializers.ModelSerializer):
    order__user_id = serializers.IntegerField(source='order.user_id', read_only=True)
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    driver_id = serializers.IntegerField(source='driver.id', read_only=True)
    order__vehicle_number = serializers.StringRelatedField(source='order.vehicle_number', read_only=True)
    order__user_id__first_name = serializers.StringRelatedField(source='order.user.first_name', read_only=True)
    order__user_id__mobile_number = serializers.StringRelatedField(source='order.user.mobile_number', read_only=True)
    status__status_name = serializers.StringRelatedField(source='status.status_name', read_only=True)
    order__otp = serializers.StringRelatedField(source='order.otp', read_only=True)
    driver__vehicle__vehicle_name = serializers.StringRelatedField(source='driver.vehicle.vehicle_name', read_only=True)
    order__total_estimated_cost = serializers.StringRelatedField(source='order.total_estimated_cost', read_only=True)
    driver__first_name = serializers.StringRelatedField(source='driver.first_name', read_only=True)
    status__colour = serializers.StringRelatedField(source='status.colour', read_only=True)
    driver__mobile_number = serializers.StringRelatedField(source='driver.mobile_number', read_only=True)
    # scheduledorder__scheduled_date_and_time = serializers.StringRelatedField(source='scheduledorder.scheduled_date_and_time', read_only=True)
    driver__vehicle__vehicle_number = serializers.StringRelatedField(source='driver.vehicle.vehicle_number', read_only=True)
    driver__vehicle__vehicletypes__vehicle_type_name = serializers.StringRelatedField(source='driver.vehicle.vehicletypes.vehicle_type_name', read_only=True)
    order__location_detail = serializers.JSONField(source='order.location_detail')

    class Meta:
        model = BookingDetail
        fields = '__all__'
