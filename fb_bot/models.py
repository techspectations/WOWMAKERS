from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Subscriber(models.Model):
	name = models.CharField(max_length = 200,default="")
	subscriptions = models.CharField(max_length = 200,default="")
	read_list = models.CharField(max_length = 200,default="") 
	is_subscribed = models.BooleanField(default = False)
	preferred_lang = models.CharField(default = "en")
	def __unicode__(self):
		return self.name + self.subscriptions
class Section(models.Model):
	name = models.CharField(max_length = 200,default = "")
