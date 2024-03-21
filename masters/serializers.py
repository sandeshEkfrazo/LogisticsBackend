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

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class FileSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filesize
        fields = '__all__'

class QueriesSerializer(serializers.ModelSerializer):
    isfor__user_role_name = serializers.StringRelatedField(source='isfor.user_role_name', read_only=True)
    class Meta:
        model = Queries
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptionplan
        fields = '__all__'

class AboutusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aboutus
        fields = '__all__'

