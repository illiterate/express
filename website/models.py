# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Address(models.Model):
    address_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    tel = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'address'


class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=255)
    company_tel = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'company'


class Delivery(models.Model):
    delivery_id = models.IntegerField(primary_key=True)
    package = models.ForeignKey('Package', models.DO_NOTHING)
    time = models.DateTimeField()
    station = models.CharField(max_length=255)
    next_station = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255)
    staff = models.ForeignKey('Staff', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'delivery'


class Package(models.Model):
    package_id = models.IntegerField(primary_key=True)
    company = models.ForeignKey(Company, models.DO_NOTHING)
    send = models.ForeignKey('User', models.DO_NOTHING, related_name='send_User')
    receive = models.ForeignKey('User', models.DO_NOTHING, related_name='receive_User')
    varity = models.CharField(max_length=255, blank=True, null=True)
    send_time = models.DateTimeField()
    receive_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'package'


class Staff(models.Model):
    staff_id = models.IntegerField(primary_key=True)
    staff_name = models.CharField(max_length=255)
    staff_tel = models.CharField(max_length=255)
    station = models.CharField(max_length=255)
    company = models.ForeignKey(Company, models.DO_NOTHING)
    password = models.CharField(max_length=255)
    duty = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'staff'


class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user'
