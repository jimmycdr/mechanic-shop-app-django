from django.contrib import admin

from maintenance.models import Specialization, MaintenanceOrder, Task, Vehicle, VehicleBrand, VehicleModel, Customer, Mechanic

class MechanicAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'cell_phone', 'specialization', 'is_active', 'is_available')
    search_fields = ('name', 'last_name', 'cell_phone', 'specialization')
    list_filter = ('is_active', 'is_available')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'cell_phone', 'email')
    search_fields = ('name', 'last_name', 'cell_phone', 'email')

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('customer', 'model', 'license_plate', 'vin', 'year', 'color', 'kilometers')
    search_fields = ('customer__name', 'model__name', 'license_plate', 'vin')
    list_filter = ('year', 'color')
    ordering = ('-year',)

class MaintenanceOrderAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'mechanic', 'start_date', 'end_date', 'status')
    search_fields = ('vehicle__license_plate', 'mechanic__name')
    list_filter = ('status',)
    ordering = ('-start_date',)

class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')
    search_fields = ('name', 'brand__name')
    list_filter = ('brand',)

admin.site.register(VehicleBrand)
admin.site.register(VehicleModel, VehicleModelAdmin)
admin.site.register(Specialization)
admin.site.register(Mechanic, MechanicAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(MaintenanceOrder)
admin.site.register(Task)
