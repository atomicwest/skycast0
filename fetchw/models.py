# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import datetime
from django.utils.translation import ugettext as _

class Query(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=3000)
    qdate = models.DateField(_("Date"), default=datetime.date.today)