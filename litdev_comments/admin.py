#coding=utf-8
from django.contrib import admin
from litdev_comments.models import Comment

# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    search_fields = ('email','nick_name','ip','comment')
    list_filter = ('create_time',)
    list_display = ('id','get_article_title','email','nick_name','ip','comment','create_time')
    fields = ('email','nick_name','ip','article','comment')
    
admin.site.register(Comment,CommentAdmin)
