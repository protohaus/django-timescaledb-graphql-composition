from django.contrib import admin

from farms.models import (
    Sensor,
    SensorReading,
    Site,
    SiteEntity,
    ControllerComponent,
    PeripheralComponent,
    PoseComponent,
    DataPointType,
    DataPoint,
)


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    pass


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteEntity)
class SiteEntityAdmin(admin.ModelAdmin):
    pass


@admin.register(ControllerComponent)
class ControllerComponentAdmin(admin.ModelAdmin):
    pass


@admin.register(PeripheralComponent)
class PeripheralComponentAdmin(admin.ModelAdmin):
    pass


@admin.register(PoseComponent)
class PoseComponentAdmin(admin.ModelAdmin):
    pass


@admin.register(DataPointType)
class DataPointTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):
    pass