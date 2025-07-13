from django.db import models
from maintenance.validators import validate_bolivia_license_plate, validate_vin, validate_vehicle_year, validate_bolivia_phone
# Create your models here.

class StatusOrder(models.TextChoices):
    NEW = 'new', 'New'
    IN_PROGRESS = 'in_progress', 'In Progress'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
    
class TaskType(models.TextChoices):
    PREVENTIVE = 'preventive', 'Preventive'
    CORRECTIVE = 'corrective', 'Corrective'
    DIAGNOSTIC = 'diagnostic', 'Diagnostic'

class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Mechanic(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cell_phone = models.CharField(max_length=10, unique=True, validators=[validate_bolivia_phone])
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cell_phone = models.CharField(max_length=10, unique=True, validators=[validate_bolivia_phone])
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"

class VehicleBrand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class VehicleModel(models.Model):
    name = models.CharField(max_length=50)
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Vehicle(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=10, unique=True, validators=[validate_bolivia_license_plate])
    vin = models.CharField(max_length=17, unique=True, validators=[validate_vin])
    year = models.PositiveIntegerField(validators=[validate_vehicle_year])
    color = models.CharField(max_length=30)
    kilometers = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.license_plate
    
class MaintenanceOrder(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusOrder.choices, default=StatusOrder.NEW)
    description = models.TextField()
    observations = models.TextField(blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Maintenance Order #{self.id} - {self.vehicle.license_plate}"

class Task(models.Model):
    maintenance_order = models.ForeignKey(MaintenanceOrder, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    task_type = models.CharField(max_length=20, choices=TaskType.choices)
    duration_hours = models.DecimalField(decimal_places=2, max_digits=4)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task #{self.id} - ({self.task_type})"