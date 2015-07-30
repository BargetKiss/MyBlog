#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.db import models
#from django.conf import settings
#from litdev_auth.models import LitdevUser

#用来修改admin中显示的app名称,因为admin app 名称是用 str.title()显示的,所以修改str类的title方法就可以实现.
class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


# Create your models here.

#状态字典
STATUS = {
    0:u'正常',
    1:u'草稿',
    2:u'删除',
}

#资讯来源
NEWS = {
    0: u'oschina',
    1: u'chiphell',
    2: u'freebuf',
    3: u'cnBeta',
}

#导航条
class Nav(models.Model):
    name = models.CharField(max_length=40,verbose_name=u'导航条内容')
    url = models.CharField(max_length=200,blank=True,null=True,verbose_name=u'指向地址')
    target_bank = models.BooleanField(u'新标签打开',default=False)
    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name=u'状态')
    rank = models.IntegerField(default= 0, verbose_name=u'排序数字')
    create_time = models.DateTimeField(u'创建时间',auto_now_add = True)
    
    class Meta:
        verbose_name_plural = verbose_name = u'导航条'
        ordering = ['-rank']
        app_label = string_with_title('blog',u'博客管理')
        
    def __str__(self):
        return self.name
        
#分类
class Category(models.Model):
    name = models.CharField(max_length=40,verbose_name=u'名称')
    parent = models.ForeignKey('self',default = None,blank=True,null=True,verbose_name = u'上级分类')
    rank = models.IntegerField(default=0,verbose_name=u'排序')
    status = models.IntegerField(default=0,choices=STATUS.items(),verbose_name=u'状态')
    create_time = models.DateTimeField(u'创建时间',auto_now_add = True)
    
    class Meta:
        verbose_name_plural = verbose_name = u'分类'
        ordering = ['rank','-create_time']
        app_label = string_with_title('blog',u'博客管理')
    
    def __str__(self):
        if self.parent:
            return '%s-->%s' % (self.parent,self.name)
        else:
            return '%s' % (self.name)
            

#标签实体类
class Tags(models.Model):
    title = models.CharField(max_length=30,verbose_name=u'标签名称',unique=True)
    add_time = models.DateTimeField(u'添加时间',auto_now_add=True)
    
    class Meta:
        verbose_name_plural = verbose_name = u'文章标签'
        ordering = ['-add_time']
        app_label = string_with_title('blog',u'标签管理')
        
    def __str__(self):
        return self.title



#文章
class Article(models.Model):
    author = models.ForeignKey('litdev_auth.LitdevUser',blank=True,null=True, verbose_name =u'作者')
    category = models.ForeignKey(Category,verbose_name=u'分类')
    title = models.CharField(max_length=100,verbose_name=u'标题')
    #en_title = models.CharField(max_length=100,verbose_name = u'英文标题')
    img = models.ImageField(upload_to='Article',default='/default.jpg',verbose_name=u'封面图片',blank=True)
    #tags = models.CharField(max_length=200,null =True,blank = True,verbose_name=u'标签',help_text=u'用逗号分隔')
    tags = models.ManyToManyField(Tags,verbose_name=u'标签')
    summary = models.TextField(verbose_name=u'摘要')
    content = models.TextField(verbose_name=u'正文')
    files = models.FileField(upload_to='files',verbose_name=u'附件',blank=True)
    
    view_times = models.IntegerField(default=0,verbose_name=u'查看数量',help_text=u'用户浏览数')
    zan_times = models.IntegerField(default=0, verbose_name=u'赞的数量',help_text=u'被赞的数量')
    
    is_top = models.BooleanField(default = False, verbose_name = u'置顶')
    rank = models.IntegerField(default= 0, verbose_name=u'排序数字')
    status = models.IntegerField(default=0, choices = STATUS.items(),verbose_name=u'状态')
    
    ding = models.IntegerField(default=0,verbose_name=u'顶的数量')
    cai = models.IntegerField(default=0,verbose_name=u'踩的数量')
    
    pub_time  = models.DateTimeField(default = False, verbose_name=u'发布时间')
    create_time = models.DateTimeField(u'创建时间',auto_now_add= True)
    update_time = models.DateTimeField(u'更新时间',auto_now_add=True)
    
    def get_tags(self):
        return self.tags.all()
        
    class Meta:
        verbose_name_plural  = verbose_name = u'文章'
        ordering = ['-is_top','rank','-pub_time','-create_time']
        app_label = string_with_title('blog',u'博客管理')
        
    
    def __str__(self):
        return self.title
		
#专栏
class Column(models.Model):
    name = models.CharField(max_length=40,verbose_name=u'专栏内容')
    summary = models.TextField(verbose_name=u'专栏摘要')
    article = models.ManyToManyField(Article,verbose_name=u'文章')
    status = models.IntegerField(default=0,choices = STATUS.items(),verbose_name=u'状态')
    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)
    
    class Meta:
        verbose_name_plural= verbose_name = u'专栏'
        ordering = ['-create_time']
        app_label = string_with_title('blog',u'博客管理')
        
    def __str__(self):
        return self.name
        

#轮播图片
class Carousel(models.Model):
    title = models.CharField(max_length=100,verbose_name=u'标题')
    summary = models.TextField(blank=True,null=True,verbose_name=u'摘要')
    img  = models.ImageField(upload_to='Carousel',verbose_name=u'轮播图片',default='/default.jpg',blank=True)
    article = models.ForeignKey(Article,verbose_name=u'文章')
    create_time = models.DateTimeField(u'创建时间',auto_now_add=True)
    
    class Meta:
        verbose_name_plural = verbose_name = u'轮播'
        ordering = ['-create_time']
        app_label = string_with_title('blog',u'博客管理')
        
    def __str__(self):
        return self.title
     
#新闻
# class News(models.Model):
#     title = models.CharField(max_length=100,verbose_name=u'标题')
#     summary = models.TextField(verbose_name=u'摘要')
#     news_from = models.IntegerField(default=0,choices=NEWS.items(),verbose_name='来源')
#     url = models.CharField(max_length=200,verbose_name=u'源地址')

#     create_time = models.DateTimeField(u'创建时间',auto_now_add=True)
#     pub_time = models.DateTimeField(default=False,verbose_name=u'发布时间')
   
    
#     class Meta:
#         verbose_name_plural = verbose_name = u'资讯'
#         ordering = ['-title']
#         app_label = string_with_title('blog',u"博客管理")


