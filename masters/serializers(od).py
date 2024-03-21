from rest_framework import serializers
from .models import *

class BookingDistanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingDistance
        fields = '__all__'


class TimeSerachSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timesearch
        fields = '__all__'