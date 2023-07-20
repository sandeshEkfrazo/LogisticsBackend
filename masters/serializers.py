from rest_framework import serializers
from .models import *

class BookingDistanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingDistance
        fields = '__all__'