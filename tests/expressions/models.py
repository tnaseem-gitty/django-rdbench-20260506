"""
Tests for F() query expression syntax.
"""
import uuid

from django.db import models


class Manager(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        app_label = 'expressions'


class Employee(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    salary = models.IntegerField(blank=True, null=True)
    manager = models.ForeignKey(Manager, models.CASCADE, null=True)

    def __str__(self):
        return '%s %s' % (self.firstname, self.lastname)

    class Meta:
        app_label = 'expressions'


class RemoteEmployee(Employee):
    adjusted_salary = models.IntegerField()

    class Meta:
        app_label = 'expressions'


class Company(models.Model):
    name = models.CharField(max_length=100)
    num_employees = models.PositiveIntegerField()
    num_chairs = models.PositiveIntegerField()
    ceo = models.ForeignKey(
        Employee,
        models.CASCADE,
        related_name='company_ceo_set',
    )
    point_of_contact = models.ForeignKey(
        Employee,
        models.SET_NULL,
        related_name='company_point_of_contact_set',
        null=True,
    )
    based_in_eu = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'expressions'


class Number(models.Model):
    integer = models.BigIntegerField(db_column='the_integer')
    float = models.FloatField(null=True, db_column='the_float')

    def __str__(self):
        return '%i, %.3f' % (self.integer, self.float)

    class Meta:
        app_label = 'expressions'


class Experiment(models.Model):
    name = models.CharField(max_length=24)
    assigned = models.DateField()
    completed = models.DateField()
    estimated_time = models.DurationField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        db_table = 'expressions_ExPeRiMeNt'
        ordering = ('name',)
        app_label = 'expressions'

    def duration(self):
        return self.end - self.start


class Result(models.Model):
    experiment = models.ForeignKey(Experiment, models.CASCADE)
    result_time = models.DateTimeField()

    def __str__(self):
        return "Result at %s" % self.result_time

    class Meta:
        app_label = 'expressions'


class Time(models.Model):
    time = models.TimeField(null=True)

    def __str__(self):
        return str(self.time)

    class Meta:
        app_label = 'expressions'


class SimulationRun(models.Model):
    start = models.ForeignKey(Time, models.CASCADE, null=True, related_name='+')
    end = models.ForeignKey(Time, models.CASCADE, null=True, related_name='+')
    midpoint = models.TimeField()

    def __str__(self):
        return "%s (%s to %s)" % (self.midpoint, self.start, self.end)

    class Meta:
        app_label = 'expressions'


class UUIDPK(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        app_label = 'expressions'


class UUID(models.Model):
    uuid = models.UUIDField(null=True)

    class Meta:
        app_label = 'expressions'
