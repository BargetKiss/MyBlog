from django.conf.urls import url
from litdev_auth.views import UserControl
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^usercontrol/(?P<slug>\w+)$', UserControl.as_view()),
    #url(r'^login/$',TemplateView.as_view(template_name="litdev_auth/login.html")),
]