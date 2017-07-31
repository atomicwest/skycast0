# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.core.urlresolvers import reverse

'''

class User(models.Model):
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    #userid will be primary key
    #profilepicture
    
    
class Query(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=100)
    
'''



class DummyUser(models.Model):
    uname = models.CharField(max_length=20)
    elmail = models.CharField(max_length=20)
    
    def __str__(self):
        return "%s : %s" % (self.uname, self.elmail)


class DummyQuery(models.Model):
    uid = models.ForeignKey(DummyUser, on_delete=models.CASCADE)
    query = models.CharField(max_length=200)
    
    def __str__(self):
        return "%s : %s"  % (str(self.uid), self.query)


class TestWeather(models.Model):
    temp = models.CharField(max_length=10)
    units = models.CharField(max_length=10)
    summary = models.CharField(max_length=1000)
    
    def __str__(self):
        return "%s %s : %s" % (self.temp, self.units, self.summary)
        
        
        