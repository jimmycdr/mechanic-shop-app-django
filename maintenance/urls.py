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
    path('maintenance-order', views.createMaintenanceOrder),
    path('maintenance-order-operations', views.MaintenanceCustomView.as_view()),
    path('set-mechanic-for-maintenance-order', views.setMechanicForMaintenanceOrder),
]