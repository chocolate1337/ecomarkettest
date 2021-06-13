from django.db.models import fields
from rest_framework import serializers

from .models import Devices, Locations


class DeviceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = ("company", "device_id", "device_model", "app", "version")


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ("latitude", "longitude", "company", "device")