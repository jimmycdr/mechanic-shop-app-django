from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'specializations', views.SpecializationViewSet)
router.register(r'mechanics', views.MechanicViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'vehicle-brands', views.VehicleBrandViewSet)
router.register(r'vehicle-models', views.VehicleModelViewSet)
router.register(r'vehicles', views.VehicleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('maintenance-order', views.MaintenanceCustomView.as_view()),
    path('maintenance-order/create', views.createMaintenanceOrder),
    path('maintenance-order/assign-mechanic', views.setMechanicForMaintenanceOrder),
    path('maintenance-order/<int:order_id>/update', views.updateMaintenanceOrder),
    path('task', views.TaskCustomView.as_view()),
    path('task/create', views.createTask),
    path('task/change-status', views.updateTaskStatus),
]