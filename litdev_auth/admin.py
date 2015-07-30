#coding:utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from litdev_auth.models import LitdevUser
from django.contrib.auth.models import User 

# Register your models here.

class LitdevUserInline(admin.StackedInline):
    model = LitdevUser
    fk_name='user'
    max_num=1

class LitdevUserAdmin(UserAdmin):
    inlines = [LitdevUserInline, ]
   

admin.site.unregister(User)
admin.site.register(User,LitdevUserAdmin)