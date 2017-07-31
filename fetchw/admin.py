# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import TestWeather, DummyUser, DummyQuery
# Register your models here.

admin.site.register(TestWeather)
admin.site.register(DummyUser)
admin.site.register(DummyQuery)