from .models import *
from  rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ScheduledOrderSerializer(serializers.ModelSerializer):
    booking__order__user__first_name = serializers.StringRelatedField(source="booking.order.user.first_name")
    booking__order__location_detail = serializers.JSONField(source="booking.order.location_detail")
    booking__order_id = serializers.IntegerField(source="booking.order.id")
    booking__total_amount = serializers.IntegerField(source="booking.total_amount")
    booking__travel_details = serializers.StringRelatedField(source="booking.travel_details")
    booking__ordered_time = serializers.StringRelatedField(source="booking.ordered_time")
    booking__driver__first_name = serializers.StringRelatedField(source="booking.driver.first_name")
    
    booking__driver_id = serializers.StringRelatedField(source="booking.driver.id")
    booking__order__user__mobile_number = serializers.StringRelatedField(source="booking.order.user.mobile_number")
    booking__order__total_estimated_cost = serializers.StringRelatedField(source="booking.order.total_estimated_cost")
    booking__status_id = serializers.StringRelatedField(source="booking.status_id")
    booking__sub_user_phone_numbers = serializers.StringRelatedField(source="booking.sub_user_phone_numbers")
    booking__order__user_id = serializers.StringRelatedField(source="booking.order.user.id")
    booking__status__status_name = serializers.StringRelatedField(source="booking.status.status_name")
    booking__driver__vehicle__vehicle_number = serializers.StringRelatedField(source="booking.driver.vehicle.vehicle_number")
    booking__driver__mobile_number = serializers.StringRelatedField(source="booking.driver.mobile_number")
    booking__driver__vehicle__vehicletypes__vehicle_type_name = serializers.StringRelatedField(source="booking.driver.vehicle.vehicletypes.vehicle_type_name")
    booking__vehicle_type__vehicle_type_name = serializers.StringRelatedField(source="booking.vehicle_type.vehicle_type_name")
    class Meta:
        model = ScheduledOrder
        fields = '__all__'