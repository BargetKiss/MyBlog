#coding=utf-8
from django.db import models
from blog.models import Article
# Create your models here.
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


#评论实体类
class Comment(models.Model):
    email = models.EmailField(verbose_name=u'评论者邮箱')
    nick_name = models.CharField(max_length=20,verbose_name=u'昵称')
    ip = models.CharField(max_length=100,verbose_name=u'评论的IP')
    article = models.ForeignKey(Article,verbose_name=u'文章')
    comment = models.TextField(verbose_name=u'内容')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name=u'评论时间')
    
    def get_ip(self):
        ip = self.ip[0:self.ip.rfind('.')]
        return ip[0:ip.rfind('.')]+'.*.*'
    
    def get_article_title(self):
        return self.article.title
    
    class Meta:
        verbose_name_plural = verbose_name = u'评论'
        ordering = ['-create_time']
        app_label = string_with_title('litdev_comments',u'评论管理')