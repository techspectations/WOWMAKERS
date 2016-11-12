from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Subscriber(models.Model):
	name = models.CharField(max_length = 200,default="")
	subscriptions = models.CharField(max_length = 200,default="")
	read_list = models.CharField(max_length = 200,default="") 
	is_subscribed = models.BooleanField(default = False)
	preferred_lang = models.CharField(default = "en",max_length=10)
	def __unicode__(self):
		return self.name + self.subscriptions


class Section(models.Model):
	code = models.CharField(max_length = 200,unique=True)
	name = models.CharField(max_length = 200,default = "")
	title = models.CharField(max_length = 200,default = "")
	category = models.CharField(max_length = 200,default = "")
	parent = models.CharField(max_length = 200,default = "")
	def __unicode__(self):
		return self.code +" "+ self.title

class Article(models.Model):
	articleID = models.CharField(max_length = 200,unique=True)
	title = models.CharField(max_length = 200,default = "")
	articleURL = models.CharField(max_length = 300,default = "")
	thumbnail = models.CharField(max_length = 400,default = "")
	summary = models.CharField(max_length = 400,default = "")
	section = models.ForeignKey(Section)
	def __unicode__(self):
		return self.title 
