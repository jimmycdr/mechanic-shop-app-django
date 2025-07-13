from rest_framework import viewsets, generics
from maintenance.models import Customer, Mechanic, MaintenanceOrder, Specialization, VehicleBrand, VehicleModel, Vehicle, Task
from maintenance.serializers import CustomerSerializer, MaintenanceOrderSerializer, MechanicSerializer, SpecializationSerializer, VehicleBrandSerializer, VehicleModelSerializer, VehicleSerializer, TaskSerializer


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer

class MechanicViewSet(viewsets.ModelViewSet):
    queryset = Mechanic.objects.all()
    serializer_class = MechanicSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class VehicleBrandViewSet(viewsets.ModelViewSet):
    queryset = VehicleBrand.objects.all()
    serializer_class = VehicleBrandSerializer

class VehicleModelViewSet(viewsets.ModelViewSet):
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class MaintenanceCustomView(generics.DestroyAPIView, generics.ListAPIView):
    queryset = MaintenanceOrder.objects.all()
    serializer_class = MaintenanceOrderSerializer

class TaskCustomView(generics.DestroyAPIView, generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
