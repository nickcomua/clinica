import datetime 
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, RangeOperators, RangeBoundary
from django.contrib.postgres.functions import TransactionNow
# Create your models here.


class Service(models.Model):
    title = models.TextField(unique=True)
    duration = models.DurationField()
    prise = models.IntegerField()
    def __str__(self) -> str:
        return self.title+" "+str(self.duration)+" "+str(self.prise)
    class Meta:
        ordering = ['title']
        constraints = [
            models.CheckConstraint(check=models.Q(
                prise__gte=0), name='prise_positive'),
            models.CheckConstraint(check=models.Q(duration__gt=datetime.timedelta(0)) & models.Q(
                duration__lte=datetime.timedelta(hours=24)), name='duration_positive'),
        ]


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user']


class Location(models.Model):
    address = models.TextField(unique=True)

    def __str__(self):
        return self.address


class Client(models.Model):
    def __str__(self):
        return self.user.username
    user = models.OneToOneField(User, on_delete=models.CASCADE)

 


class TsTzRange(models.Func):
    function = 'TSTZRANGE'
    output_field = DateTimeRangeField() 


class Appointement(models.Model):
    class Meta: 
        ordering = ['start_datetime']
        constraints = [
            ExclusionConstraint(
                name='exclude_overlapping_reservations',
                expressions=(
                    (TsTzRange('start_datetime', 'end_datetime', RangeBoundary()), RangeOperators.OVERLAPS),
                    ('location', RangeOperators.EQUAL),
                ),
            ),
            ExclusionConstraint(
                name='exclude_overlapping_clientss',
                expressions=(
                    (TsTzRange('start_datetime', 'end_datetime', RangeBoundary()), RangeOperators.OVERLAPS),
                    ('client', RangeOperators.EQUAL),
                ),
            ),
            ExclusionConstraint(
                name='exclude_overlapping_workers',
                expressions=(
                    (TsTzRange('start_datetime', 'end_datetime', RangeBoundary()), RangeOperators.OVERLAPS),
                    ('worker', RangeOperators.EQUAL),
                ),
            ), 
        ]
    
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField() 
    end_datetime = models.DateTimeField() 

    # def _get_end_datetime(self):
    #     return self.start_datetime + self.service.models.DurationField(_("Duration"))
    # end_datetime = property(_get_end_datetime)
