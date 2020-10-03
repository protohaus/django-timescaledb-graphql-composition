import uuid
from datetime import timedelta, datetime

from django.db import models, IntegrityError, connection
from django.utils.dateparse import parse_datetime


class Sensor(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class SensorReading(models.Model):
    time = models.DateTimeField(primary_key=True, default=datetime.now)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()

    def save(self, *args, **kwargs):
        self.save_and_smear_timestamp(*args, **kwargs)

    def save_and_smear_timestamp(self, *args, **kwargs):
        """Recursivly try to save by incrementing the timestamp on duplicate error"""
        try:
            super().save(*args, **kwargs)
        except IntegrityError as exception:
            # Only handle the error:
            #   psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "1_1_farms_sensorreading_pkey"
            #   DETAIL:  Key ("time")=(2020-10-01 22:33:52.507782+00) already exists.
            if all(k in exception.args[0] for k in ("Key", "time", "already exists")):
                # Increment the timestamp by 1 µs and try again
                self.time = str(parse_datetime(self.time) + timedelta(microseconds=1))
                self.save_and_smear_timestamp(*args, **kwargs)

    def __str__(self):
        return f"{self.value}@{self.time}"


class Site(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class SiteEntity(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ControllerComponent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    site_entity = models.OneToOneField(SiteEntity, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Controller of SE {self.site_entity.name}"


class PeripheralComponent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    site_entity = models.OneToOneField(SiteEntity, on_delete=models.CASCADE)
    controller_component = models.ForeignKey(
        ControllerComponent, on_delete=models.CASCADE
    )
    config = models.JSONField()

    def __str__(self):
        return f"Peripheral of SE {self.site_entity.name}"


class PoseComponent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    site_entity = models.OneToOneField(
        SiteEntity, on_delete=models.CASCADE, related_name="pose_component"
    )
    relative_to = models.ForeignKey(
        SiteEntity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="dependent_pose_components",
    )
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    z = models.FloatField(default=0)

    def __str__(self):
        return f"Pose of SE {self.site_entity.name}"


class DataPointType(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} in {self.unit}"


class DataPoint(models.Model):
    time = models.DateTimeField(primary_key=True, default=datetime.now)
    peripheral = models.ForeignKey(PeripheralComponent, on_delete=models.CASCADE)
    data_type = models.ForeignKey(DataPointType, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f"{self.value} {self.data_type.unit} from {self.peripheral.site_entity.name}"
