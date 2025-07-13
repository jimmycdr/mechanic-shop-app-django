from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from .models import Mechanic, MaintenanceOrder
from .serializers import MechanicSerializer

class MechanicViewSet(viewsets.ModelViewSet):
    queryset = Mechanic.objects.all()
    serializer_class = MechanicSerializer

@api_view(['POST'])
def createMaintenanceOrder(request):
    try:
        MaintenanceOrder.objects.create(**request.data)
        return JsonResponse({"detail": "Maintenance order created successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)