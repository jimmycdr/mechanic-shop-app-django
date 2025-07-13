from django.http import JsonResponse
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from .models import Customer, Mechanic, MaintenanceOrder, Specialization, StatusOrder, VehicleBrand, VehicleModel, Vehicle
from .serializers import CustomerSerializer, MaintenanceOrderSerializer, MechanicSerializer, SetMechanicForMaintenanceOrderSerializer, SpecializationSerializer, VehicleBrandSerializer, VehicleModelSerializer, VehicleSerializer

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

def assign_mechanic_or_none(mechanic_id=None):
    if mechanic_id:
        try:
            mechanic = Mechanic.objects.get(pk=mechanic_id)
        except Mechanic.DoesNotExist:
            raise Mechanic.DoesNotExist("Mechanic not found")
        
        if not mechanic.is_active or not mechanic.is_available:
            raise ValueError("Mechanic is not available or not active.")
        
        return mechanic
    else:
        mechanic = Mechanic.objects.filter(is_active=True, is_available=True).first()
        return mechanic

def check_existing_order(data):
    vehicle_id = data.get('vehicle')
    if vehicle_id:
        existing_order = MaintenanceOrder.objects.filter(
            vehicle_id=vehicle_id,
            status__in=[StatusOrder.NEW, StatusOrder.IN_PROGRESS]
        ).first()
        if existing_order:
            return f"Vehicle already has an active maintenance order (Order ID: {existing_order.id})"
    return None

@api_view(['POST'])
def createMaintenanceOrder(request):
    try:
        serializer = MaintenanceOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse({"errors": serializer.errors}, status=400)

        duplicate_error = check_existing_order(request.data)
        if duplicate_error:
            return JsonResponse({"error": duplicate_error}, status=400)
        
        mechanic_id = request.data.get('mechanic')
        mechanic = None

        if mechanic_id:
            try:
                mechanic = assign_mechanic_or_none(mechanic_id)
            except Mechanic.DoesNotExist:
                return JsonResponse({"error": "Mechanic not found"}, status=404)
            except ValueError as e:
                return JsonResponse({"warning": str(e)}, status=200)
        order = serializer.save(mechanic=mechanic)
        if mechanic:
            mechanic.is_available = False
            mechanic.save()
            return JsonResponse({
                "message": "Order created and mechanic assigned successfully",
                "order_id": order.id,
                "mechanic_id": mechanic.id,
                "mechanic_name": f"{mechanic.name} {mechanic.last_name}"
            }, status=201)
        else:
            return JsonResponse({
                "message": "Order created without assigning a mechanic",
                "order_id": order.id
            }, status=201)

    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)
    
@api_view(['POST'])
def setMechanicForMaintenanceOrder(request):
    serializer = SetMechanicForMaintenanceOrderSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse({"errors": serializer.errors}, status=400)

    order_id = serializer.validated_data.get("order_id")
    mechanic_id = serializer.validated_data.get("mechanic_id")

    try:
        order = MaintenanceOrder.objects.get(pk=order_id)
    except MaintenanceOrder.DoesNotExist:
        return JsonResponse({"error": "Order not found"}, status=404)

    if order.status not in [StatusOrder.NEW, StatusOrder.IN_PROGRESS]:
        return JsonResponse({
            "error": f"Cannot assign mechanic to order with status: {order.status}"
        }, status=400)
        
    try:
        mechanic = assign_mechanic_or_none(mechanic_id)
    except Mechanic.DoesNotExist:
        return JsonResponse({"error": "Mechanic not found"}, status=404)
    except ValueError as e:
        return JsonResponse({"warning": str(e)}, status=200)
    if not mechanic:
        return JsonResponse({"error": "Mechanic not available"}, status=400)

    order.mechanic = mechanic
    order.save()

    mechanic.is_available = False
    mechanic.save()
    return JsonResponse({
        "message": "Mechanic assigned successfully",
        "order_id": order.id,
        "mechanic_id": mechanic.id,
        "mechanic_name": f"{mechanic.name} {mechanic.last_name}"
    }, status=200)