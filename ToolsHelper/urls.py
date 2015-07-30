from django.conf.urls import url

urlpatterns = [
    url(r'^upload_textarea/(?P<spath>\w+)','ToolsHelper.views.upload_textarea'),
    url(r'^view_textarea$','ToolsHelper.views.view_textarea'),  
]