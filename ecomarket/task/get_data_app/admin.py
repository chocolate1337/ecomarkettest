from django.contrib import admin
from .models import Companies, Devices, Locations, Couriers



@admin.register(Couriers)
class AdminCouriers(admin.ModelAdmin):
    list_display = ("phone", "full_name", "address")

@admin.register(Devices)
class AdminDevices(admin.ModelAdmin):
    list_display = ("device_model", "company", "device_id", "courier")
    list_filter = ("company", "courier")

@admin.register(Companies)
class AdminCompanies(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")


@admin.register(Locations)
class AdminLocations(admin.ModelAdmin):
    list_display = ("latitude", "longitude", "company", "device")
    list_filter = ("company", "device")







