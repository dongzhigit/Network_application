#/usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

class AppLog(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=111, blank=True)
    department = models.CharField(max_length=111, blank=True)
    claimant = models.CharField(db_column='Claimant', max_length=111, blank=True) # Field name made lowercase.
    company = models.CharField(max_length=111, blank=True)
    mac = models.CharField(max_length=111, blank=True)
    project = models.CharField(max_length=111, blank=True)
    begintime = models.DateField(blank=True, null=True)
    endtime = models.DateField(blank=True, null=True)
    operation_time = models.DateTimeField(blank=True, null=True)
    stats = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=111, blank=True)
    class Meta:
        managed = False
        db_table = 'app_log'

class OpenvpnLog(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=111, blank=True)
    mail = models.CharField(max_length=111, blank=True)
    department = models.CharField(max_length=111, blank=True)
    notes = models.CharField(max_length=111, blank=True)
    time = models.DateTimeField(blank=True, null=True)
    stats = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=111, blank=True)
    class Meta:
        managed = False
        db_table = 'openvpn_log'