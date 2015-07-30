#coding=utf-8
from django.contrib import admin
from blog.models import Article,Category,Carousel,Nav,Column,Tags #,News

# Register your models here.

#分类后台管理
class CategoryAdmin(admin.ModelAdmin):
    search_fields= ('name'),
    list_filter = ('status','create_time')
    list_display= ('name','parent','rank','status')
    fields= ('name','parent','rank','status')

#文章后台管理
class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('title','summary')
    list_filter = ('status','category','is_top','create_time','update_time')
    list_display = ('title','category','author','status','is_top','ding','cai','update_time')
    filter_horizontal = ['tags']
    #对录入的字段进行分组、加框的作用
    fieldsets = (
        (u'基本信息',{
            'fields':('title','img','category','tags','author','is_top','rank','status','files')
        }),
        (u'摘要',{
            'fields':('summary',)
        }),
        (u'内容',{
            'fields':('content',)
        }),        
        (u'时间',{
            'fields':('pub_time',)
        })
    )
    
#标签后台管理
class TagsAdmin(admin.ModelAdmin):
    search_fields =('title',)
    list_display = ('id','title','add_time')
    
    


#导航管理
class NavAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name','url','target_bank','status','rank','create_time')
    list_filter = ('status','create_time')
    fields = ('name','url','target_bank','rank','status')
    
#专栏管理
class ColumnAdmin(admin.ModelAdmin):
    search_fields =  ('name',)
    list_display = ('name','status','create_time')
    list_filter = ('status','create_time')
    fields = ('name','status','article','summary')
    filter_horizontal = ('article',)
  
#图片轮播管理
class CarouselAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title','article','img','create_time')
    list_filter = ('create_time',)
    fields = ('title','article','img','summary')


# class NewsAdmin(admin.ModelAdmin):
#     search_fields = ('title','summary')
#     list_filter = ('news_from','create_time')
#     list_display = ('title','news_from','url','create_time')
#     fields = ('title','news_from','url','summary','pub_time')


admin.site.register(Category,CategoryAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Nav,NavAdmin)
admin.site.register(Column,ColumnAdmin)
admin.site.register(Carousel,CarouselAdmin)
admin.site.register(Tags,TagsAdmin)
#admin.site.register(News,NewsAdmin)