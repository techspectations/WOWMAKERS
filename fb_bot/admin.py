from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Subscriber)
admin.site.register(Section)
admin.site.register(Article)