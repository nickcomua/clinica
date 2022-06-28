from unicodedata import name
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
    function = 'daterange'
    output_field = DateTimeRangeField()
    arguments = [ models.DateTimeField(), models.DateTimeField() ]

class TsTzRange(models.Func):
    function = 'TSTZRANGE'
    output_field = DateTimeRangeField()

class AddTimeFunc(models.Func):
    function = "DATEADD"
    output_field = models.DateTimeField()
    arguments = [models.DateTimeField(), models.DurationField()]


class Appointement(models.Model):
    class Meta:
        ordering = ['datetime']
        constraints = [
            ExclusionConstraint(
                name='exclude_overlapping_reservations', 
                expressions=(
                    ('datetime', RangeOperators.OVERLAPS),
                    ('location', RangeOperators.EQUAL),
                ), 
            ),
        ]
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    datetime = DateTimeRangeField() 
    # @property
    # def end_datetime(self):
    #     return self.start_datetime + self.service.duration 

    # def _get_end_datetime(self):
    #     return self.start_datetime + self.service.models.DurationField(_("Duration"))
    # end_datetime = property(_get_end_datetime)

