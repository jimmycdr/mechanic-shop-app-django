from rest_framework import serializers
from .models import Mechanic, StatusOrder, MaintenanceOrder, Customer

class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mechanic
        fields = '__all__'

class StatusOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusOrder
        fields = '__all__'

class MaintenanceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceOrder
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
