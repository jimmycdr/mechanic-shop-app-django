from django.http import JsonResponse
from rest_framework.decorators import api_view
from maintenance.models import Mechanic, MaintenanceOrder, StatusOrder, Task, StatusTask
from maintenance.serializers import MaintenanceOrderPutSerializer, MaintenanceOrderSerializer, SetMechanicForMaintenanceOrderSerializer, TaskSerializer

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
        data_req = MaintenanceOrderSerializer(data=request.data)
        if not data_req.is_valid():
            return JsonResponse({"errors": data_req.errors}, status=400)

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
        order = data_req.save(mechanic=mechanic)
        if mechanic:
            mechanic.is_available = False
            mechanic.save()
            return JsonResponse({
                "message": "Maintenance order created and mechanic assigned successfully",
                "order_id": order.id,
                "mechanic_id": mechanic.id,
                "mechanic_name": f"{mechanic.name} {mechanic.last_name}"
            }, status=201)
        else:
            return JsonResponse({
                "message": "Maintenance order created without assigning a mechanic",
                "order_id": order.id
            }, status=201)

    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)
    
@api_view(['POST'])
def setMechanicForMaintenanceOrder(request):
    data_req = SetMechanicForMaintenanceOrderSerializer(data=request.data)
    if not data_req.is_valid():
        return JsonResponse({"errors": data_req.errors}, status=400)

    order_id = data_req.validated_data.get("order_id")
    mechanic_id = data_req.validated_data.get("mechanic_id")

    try:
        order = MaintenanceOrder.objects.get(pk=order_id)
    except MaintenanceOrder.DoesNotExist:
        return JsonResponse({"error": "Maintenance order not found"}, status=404)

    if order.status not in [StatusOrder.NEW, StatusOrder.IN_PROGRESS]:
        return JsonResponse({
            "error": f"Cannot assign mechanic to Maintenance order with status: {order.status}"
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

@api_view(['PUT'])
def updateMaintenanceOrder(request, order_id):

    try:
        order = MaintenanceOrder.objects.get(pk=order_id)
    except MaintenanceOrder.DoesNotExist:
        return JsonResponse({"error": "Maintenance order not found"}, status=404)

    if order.status not in [StatusOrder.NEW, StatusOrder.IN_PROGRESS]:
        return JsonResponse({
            "error": f"Cannot update Maintenance order with status: {order.status}. Only NEW or IN_PROGRESS orders can be updated."
        }, status=400)
    
    data_req = MaintenanceOrderPutSerializer(order, data=request.data, partial=True)
    if not data_req.is_valid():
        return JsonResponse({"errors": data_req.errors}, status=400)
    
    data_req.save()
    return JsonResponse({"message": "Maintenance order updated successfully"}, status=200)

@api_view(['POST'])
def createTask(request):
    serializer = TaskSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse({"errors": serializer.errors}, status=400)

    order_id = request.data.get("maintenance_order")
    try:
        order = MaintenanceOrder.objects.get(pk=order_id)
    except MaintenanceOrder.DoesNotExist:
        return JsonResponse({"error": "Maintenance order not found"}, status=404)

    if order.status != StatusOrder.IN_PROGRESS:
        return JsonResponse({"error": "Maintenance order must be in progress to add tasks"}, status=400)

    task = serializer.save()
    return JsonResponse({
        "message": "Task created successfully",
        "task_id": task.id
    }, status=201)

@api_view(['PUT'])
def updateTaskStatus(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    new_status = request.data.get("status")
    if new_status not in StatusTask.values:
        return JsonResponse({"error": "Invalid status"}, status=400)

    task.status = new_status
    task.save()

    if new_status == StatusTask.COMPLETED:
        order = task.maintenance_order
        order.total_cost += task.cost or 0
        order.save()

        incomplete_tasks = order.tasks.exclude(status=StatusTask.COMPLETED)
        if not incomplete_tasks.exists():
            order.status = StatusOrder.COMPLETED
            order.save()

    return JsonResponse({"message": "Task status updated successfully"}, status=200)