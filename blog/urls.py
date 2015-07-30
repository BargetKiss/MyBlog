#coding=utf-8
from django.conf.urls import url
from blog.views import IndexView,ArticleView,UserView,AllView,CategoryView,TagView,SearchView
from django.views.generic import TemplateView,DetailView

urlpatterns = [
    url(r'^$',IndexView.as_view()),
    url(r'^article/(?P<pk>\d+).html$',ArticleView.as_view()),
    #url(r'^user/(?P<slug>\w+)$',UserView.as_view()),
    #url(r'^register/$',TemplateView.as_view(template_name="blog/register.html")),
    #url(r'^login/$',TemplateView.as_view(template_name="blog/login.html")),
    #url(r'^forgetpassword/$',TemplateView.as_view(template_name="blog/forgetpassword.html")),
    #url(r'^resetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)$',TemplateView.as_view(template_name="blog/resetpassword.html")),
    url(r'^all/$',AllView.as_view()),
    url(r'^category/(?P<id>\d+)/$',CategoryView.as_view()),
    url(r'^tag/(?P<id>\d+)/$',TagView.as_view()),
    url(r'^search/$',SearchView.as_view()),
]