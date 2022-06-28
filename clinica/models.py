from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, RangeOperators, RangeBoundary
# Create your models here.


class Service(models.Model):
    title = models.TimeField()
    duration = models.DurationField()
    prise = models.IntegerField()

    class Meta:
        ordering = ['title']


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)

    class Meta:
        ordering = ['user']


class Location(models.Model):
    address = models.TextField()


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class DateRangeFunc(models.Func):
    function = "daterange"
    output_field = DateTimeRangeField()


class Appointement(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    #@property
    # def end_datetime(self):
    #    return self.start_datetime + self.service.models.DurationField(_("Duration")) 
    class Meta:
        ordering = ['start_datetime']
        constraints = [
            ExclusionConstraint(
                name='appointement_datetime_exclusion',
                expressions=[
                    (
                        DateRangeFunc(
                            "start_datetime", "start_datetime"+"duration", RangeBoundary()
                        ),
                        RangeOperators.OVERLAPS,
                    ),
                    ('loaction', RangeOperators.EQUAL)
                ]
                # condition=models.Q(start_datetime__range=models.F('duration')),
            ),
        ]
