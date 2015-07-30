#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.core.exceptions import PermissionDenied
import litdev_comments.models as DBModel
from MyBlog.settings import COMMENTS_ENABLE
from django.core.cache import caches
import logging

try:
    cache = caches['memcache']
except ImportError as e:
    cache = caches['default']
    

logger = logging.getLogger(__name__)

from blog.models import Article as ArticleModel 

# Create your views here.

class CommentControl(View):
    
    def post(self,request,*args,**kwargs):
        if not COMMENTS_ENABLE:
            return HttpResponse(u'暂时关闭评论功能.',status=403)
        
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
            
        self.cur_user_ip = ip
        visited_ips = cache.get('comment_ips',[])
        
        if ip in visited_ips:
            return HttpResponse(u'两次评论间隔不能小于5分钟',status=403)
        
        
        email = self.request.POST.get("email","unknow@unknow.com")
        nick_name = self.request.POST.get("nick_name","")    
        article_id = self.kwargs.get('slug',0)       
        comment = self.request.POST.get("comment","")
        if not comment:
            return HttpResponse(u'请输入评论内容',status=403)
        if not nick_name:
            return HttpResponse(u'请输入您的称呼',status=403)
        if not email:
            return HttpResponse(u'请输入您的邮箱',status=403)        
        
        try:
            article = ArticleModel.objects.get(id=int(article_id))
        except ArticleModel.DoesNotExist:
            raise PermissionDenied
            #return HttpResponse(u'文章不存在',status=403)
        
        comment_obj = DBModel.Comment.objects.create(email=email,nick_name=nick_name,ip=ip,article=article,comment=comment)
        
        try:
            comment_id = comment_obj.id
            visited_ips.append(ip)
            cache.set('comment_ips',visited_ips,5*60)
        except Exception as e:
            logger.error(u'评论添加失败:%s' % e.message)
        
        #返回当前评论内容
        html = "<li>\
                    <div class=\"vmaig-comment-tx\">\
                        <img src='http://vmaig.qiniudn.com/image/tx/tx-default.jpg' width=\"40\"></img>\
                    </div>\
                    <div class=\"vmaig-comment-content\">\
                        <a><h1>"+comment_obj.nick_name+"</h1></a>"\
                        +u"<p>评论："+comment_obj.comment+"</p>"+\
                        "<p>"+comment_obj.create_time.strftime("%Y-%m-%d %H:%I:%S")+"</p>\
                    </div>\
                </li>"
        
        return HttpResponse(html)
            
        