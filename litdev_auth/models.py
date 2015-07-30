#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class LitdevUser(models.Model):
    user = models.OneToOneField(User,unique=True)
    img = models.ImageField(upload_to='HeadImg', default='/static/tx/default.jpg',verbose_name=u'头像地址',blank=True)
    intro = models.CharField(max_length=200,blank=True,null=True,verbose_name=u'简介')
    
    class Meta:
        verbose_name_plural= verbose_name = u'用户拓展信息'

    def user_name(self):
        return self.user.username
    
    def __str__(self):
        return self.user.username
