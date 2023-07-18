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

class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
