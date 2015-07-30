#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.views.generic import View
from django.core.mail import send_mail
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.http import base36_to_int, is_safe_url,urlsafe_base64_decode,urlsafe_base64_encode
from litdev_auth.models import LitdevUser
from django.contrib.auth.models import User
from litdev_auth.forms import LitdevPasswordResetForm,LitdevCreationForm
import datetime, time
from PIL import Image
import os
import json
import base64
import logging

logger = logging.getLogger(__name__)

# Create your views here.

class UserControl(View):
    
    def get(self,request,*args,**kwargs):
        #如果是get请求，直接返回404
        raise Http404
        
    #POST请求
    def post(self,request,*args,**kwargs):
        
        #操作类型
        slug = self.kwargs.get('slug')
        
        if slug == 'login':
            return self.login(request)
        elif slug =='logout':
            return self.logout(request)
        elif slug == 'changepassword':
            return self.changepassword(request)
        elif slug == 'forgetpassword':
            return self.forgetpassword(request)
        elif slug =='resetpassword':
            return self.resetpassword(request)
            
        raise PermissionDenied
        
    
    
    #登陆###########################
    def login(self,request):
        if request.user.is_authenticated():
            raise PermissionDenied
            
        username = request.POST.get("username","")
        password = request.POST.get("password","")
        user = auth.authenticate(username=username,password=password)
        
        errors = []
        
        if user is not None:
            auth.login(request,user)
        else:
            errors.append("密码或者用户名不正确")
            
        mydict = {"errors":errors}
        
        return HttpResponse(json.dumps(mydict),content_type="application/json")
        
    
    
    #登出############################
    def logout(self,request):
        if not request.user.is_authenticated():
            raise PermissionDenied
        else:
            auth.logout(request)
            return HttpResponse('OK')
            
            
    #修改密码#########################
    def changepassword(self,request):
        
        if not request.user.is_authenticated():
            raise PermissionDenied 
        form = PasswordChangeForm(request.user,request.POST)
        errors = []
        
        #验证表单是否正确
        if form.is_valid():
            user = form.save()
            auth.logout(request)
        else:
            #如果表单不正确，保存错误到errors列表中
            for k,v in form.errors.items():
                errors.append(v.as_text())
                
        mydict = {"errors":errors}
        return HttpResponse(json.dumps(mydict),content_type="application/json")
        
    #找回密码####################
    def forgetpassword(self,request):
        username = self.request.POST.get("username","")
        email = self.request.POST.get("email","")
        
        form = LitdevPasswordResetForm(request.POST)
        
        errors =[]
        
        
        #验证表单是否正确
        if form.is_valid():
            token_generator = default_token_generator
            from_email = None
            
            opts = {
                'token_generator':token_generator,
                'from_email':from_email,
                'request':request,
            }
            user = form.save(**opts)
        else:
            #如果表单不正确，保存错误到errors列表中
            for k,v in form.errors.items():
                #v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())
                
        mydict = {"errors":errors}
        return HttpResponse(json.dumps(mydict),content_type="application/json")
       

    #密码重置
    def resetpassword(self,request):
        uidb64 = self.request.POST.get("uidb64","")
        token = self.request.POST.get("token","")
        password1 = self.request.POST.get("password1","")
        password2 = self.request.POST.get("password2","")
        
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(id=uid)
        except (TypeError,ValueError,OverflowError,User.DoesNotExist):
            user = None
        
        token_generator  = default_token_generator
        if user is not None and token_generator.check_token(user,token):
            form = SetPasswordForm(user,request.POST)
            error = []
            if form.is_valid():
                user = form.save()
            else:
                #如果表单不正确，保存错误到errors列表中
                for k,v in form.errors.items():
                    errors.append(v.as_text())
                    
        else:
            return HttpResponse("密码重设失败！\n密码重置链接无效，可能因为它已使用。可以请求一次新的密码重设.",status=403)
            
        