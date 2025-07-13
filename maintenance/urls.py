from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'mechanics', views.MechanicViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('maintenance-order/', views.createMaintenanceOrder),
]