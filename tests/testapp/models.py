# -*- coding:utf-8 -*-

from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=30)
    social_security_number = models.CharField(max_length=30, null=True, blank=True)
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.name
