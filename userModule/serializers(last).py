from .models import *
from  rest_framework import serializers

class ScheduledOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledOrder
        fields = '__all__'