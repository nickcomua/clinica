from rest_framework import serializers
from clinica.models import *  
from django.contrib.auth.models import User 
class UserSerializer(serializers.ModelSerializer):
    #snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    class Meta:
        model = User
        fields = ['id', 'username']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'duration', 'prise']


class WorkerSerializer(serializers.ModelSerializer):
    services_detail = ServiceSerializer(
        many=True, read_only=True, source='services')
    user_details = UserSerializer(read_only=True, source='user')
    #appoiments = AppointementSerializer(many=True, read_only=True)

    class Meta:
        model = Worker
        fields = ['id', 'user', 'user_details', 'services', 'services_detail'] 


class ClientSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(read_only=True, source='user')

    class Meta:
        model = Client
        fields = ['id', 'user', 'user_data']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'address']


class AppointementSerializer(serializers.ModelSerializer):
    client_data = ClientSerializer(read_only=True, source='client')
    worker_data = WorkerSerializer(read_only=True, source='worker')
    location_data = LocationSerializer(read_only=True, source='location')
    service_data = ServiceSerializer(read_only=True, source='service')  

    class Meta:
        model = Appointement
        fields = ['id', 'client', 'client_data', 'worker', 'worker_data',
                  'location', 'location_data', 'service', 'service_data', 'start_datetime', 'end_datetime']