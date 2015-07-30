#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,Http404
from django import template
from django.core.cache import caches
from django.views.generic import View,TemplateView,ListView,DetailView
from MyBlog.settings import PAGE_NUM
from django.core.exceptions import PermissionDenied
import blog.models as DBModel
from litdev_comments.models import Comment as DBComment
from django.db.models import Q
import json
import logging
import time,datetime

try:
    cache = caches['memcache']
except ImportError as e:
    cache = caches['default']
    
logger = logging.getLogger(__name__)

# Create your views here.
class BaseClass(object):
    
    def get_context_data(self,*args,**kwargs):
        context  = super(BaseClass,self).get_context_data(**kwargs)
        
        try:
            #热门
            context['hot_article_list'] =DBModel.Article.objects.order_by('-view_times')[0:10]
            
            #导航列表
            context['nav_list'] = DBModel.Nav.objects.filter(status=0)
            
            #最新
            context['latest_comment_list'] = DBComment.objects.order_by('-create_time')[0:10]
            
            #标签云
            context['tags_list'] = DBModel.Tags.objects.all()
            
        except Exception as e:
            logger.error(u'[BaseClass]加载基本信息出错: %s ' % e)
            
        return context

###首页视图##########
class IndexView(BaseClass,ListView):
    template_name = 'blog/index.html'
    # context_object_name = 'article_list'
    # paginate_by = PAGE_NUM
    
    def get_context_data(self,**kwargs):
        #轮播
        kwargs['carousel_page_list'] = DBModel.Carousel.objects.all()
        
        return super(IndexView,self).get_context_data(**kwargs)
        
    def get_queryset(self):
        article_list = DBModel.Article.objects.filter(status=0)
        return article_list
        

#获取所有
class AllView(BaseClass,ListView):
    template_name = 'blog/all.html'
    context_object_name = 'article_list'
    
    def get_context_data(self,**kwargs):
        kwargs['category_list'] = DBModel.Category.objects.all()
        kwargs['PAGE_NUM'] = PAGE_NUM
        return super(AllView,self).get_context_data(**kwargs)
        
    def get_queryset(self):
        article_list = DBModel.Article.objects.filter(status=0)[0:PAGE_NUM]
        return article_list
        
    def post(self,request,*args,**kwargs):
        val = self.request.POST.get("val","")
        sort = self.request.POST.get("sort","time")
        start = int(self.request.POST.get("start",0))
        end = int(self.request.POST.get("end",PAGE_NUM))
        
        if sort == "time":
            sort = "-pub_time"
        elif sort == "recommend":
            sort = "-view_times"
        else:
            sort == "-pub_time"
        if val == "all":
            article_list = DBModel.Article.objects.filter(status =0).order_by(sort)[start:end+1]
        else:
            try:
                article_list = DBModel.Category.objects.get(name=val).article_set.filter(status=0).order_by(sort)[start:end+1]
            except DBModel.Category.DoesNotExist:
                raise PermissionDenied 
        
        isend = len(article_list) != (end-start+1)
        
        article_list = article_list[0:end-start]
        html=""
        for article in article_list:
            html += template.loader.get_template('blog/include/all_post.html').render(template.Context({'post':article}))
            
        mydict = {"html":html,"isend":isend}
        
        return HttpResponse(json.dumps(mydict),content_type="application/json")

#######文章详情##########    
class ArticleView(BaseClass,DetailView):
    queryset = DBModel.Article.objects.filter(status=0)
    template_name = 'blog/article.html'
    
    def get(self,request,*args,**kwargs):
        #统计文章的访问次数
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
            
        self.cur_user_ip = ip
        
        
        article_id = self.kwargs.get('pk')
        #获取 15*60s时间内访问过这篇文章的所有ip
        visited_ips = cache.get('article_%s' % str(article_id),[])
        #print('--------------article_%s' % str(article_id))
        #如果ip不存在就把文章的浏览次数+1
        if ip not in visited_ips:
            try:
                article_entity = self.queryset.get(id = int(article_id))
            except Article.DoesNotExist:
                #logger.error(u'访问不存在的文章:[%s]' % str(article_id))
                raise Http404
            else: #如果没有发生异常
                 article_entity.view_times += 1
                 article_entity.save()
                 visited_ips.append(ip)
            #print('--------------'+str(len(visited_ips)))   
            #更新缓存
            cache.set('article_%s' % str(article_id),visited_ips,15*60)
            
        return super(ArticleView,self).get(request,*args,**kwargs)
        
        
    def get_context_data(self,**kwargs):
        #评论
        article_id = self.kwargs.get('pk')
        kwargs['comment_list'] = self.queryset.get(id=article_id).comment_set.all()
        return super(ArticleView,self).get_context_data(**kwargs)
        
    
#用户管理中心#############    
class UserView(BaseClass,TemplateView):
    template_name = 'blog/user.html'
    
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated():
            return render(request,'blog/login.html')
            
        slug = self.kwargs.get('slug')
        
        if slug =='changetx':
            self.template_name = 'blog/user_changetx.html'
            return super(UserView,self).get(request,*args,**kwargs)
        elif slug == 'changepassword':
            self.template_name = 'blog/user_changepassword.html'
            return super(UserView,self).get(request,*args,**kwargs)
        elif slug == 'changeinfo':
            self.template_name = 'blog/user_changeinfo.html'
            return super(UserView,self).get(request,*args,**kwargs)
        elif slug == 'message':
            self.template_name = 'blog/user_message.html'
            return super(UserView,self).get(request,*args,**kwargs)
          
        logger.error(u'[UserView]不存在此%s接口' % slug)  
        raise Http404
        
#分类
class CategoryView(BaseClass,ListView):
    template_name='blog/category.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM
    
    def get_queryset(self):
        uid = self.kwargs.get('id',0)
        try:
            article_list = DBModel.Category.objects.get(id=uid).article_set.all()
        except DBModel.Category.DoesNotExist:
            raise Http404
            
        return article_list
        
        
#标签
class TagView(BaseClass,ListView):
    template_name = 'blog/tag.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM
    
    def get_queryset(self):
        t_id = self.kwargs.get('id',0)
        try:
            article_list = DBModel.Tags.objects.get(id=t_id).article_set.all()
        except DBModel.Tags.DoesNotExist:
            raise Http404
        
        return article_list


#搜索视图
class SearchView(BaseClass,ListView):
    template_name= 'blog/search.html'
    context_object_name = 'article_list'
    paginate_by = PAGE_NUM
    
    def get_context_data(self,**kwargs):
        kwargs['s'] = self.request.GET.get('s','')
        return super(SearchView,self).get_context_data(**kwargs)
        
    def get_queryset(self):
        s = self.request.GET.get('s','')
        article_list = DBModel.Article.objects.only('title','summary').filter(Q(title__icontains=s)|Q(summary__icontains=s),status=0)
        return article_list