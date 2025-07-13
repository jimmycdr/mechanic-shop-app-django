from rest_framework import serializers
from .models import Mechanic, MaintenanceOrder, Customer, Specialization, Vehicle, VehicleBrand, VehicleModel

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'
class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mechanic
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = '__all__'

class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class MaintenanceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceOrder
        fields = '__all__'

class SetMechanicForMaintenanceOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    mechanic_id = serializers.IntegerField()