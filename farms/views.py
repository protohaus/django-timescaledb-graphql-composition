from datetime import datetime, timedelta, timezone

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from farms.models import SensorReading, Sensor, DataPoint

# Create your views here.


class CreateSensorReadingView(View):
    def post(self, request, *args, **kwargs):
        # sensor = Sensor.objects.get(id="f1a1febd-10e7-4012-a655-2dee7c15b049")
        # sensor_reading = SensorReading.objects.create(
        #     time="2020-10-01 22:33:52.507782+00:00",
        #     sensor=sensor,
        #     value=float(request.POST["value"]),
        # )
        # return HttpResponse(content=sensor_reading)
        find_site = Q(peripheral__site_entity__site=request.POST["site"])
        prev_time = Q(time__gt=datetime.now(tz=timezone.utc) - timedelta(minutes = 20))
        data_points = DataPoint.objects.filter(find_site & prev_time)
        print(data_points.query)
        return HttpResponse(content=data_points)
